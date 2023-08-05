import time
import math
from collections import namedtuple
from random import random

import RPi.GPIO as GPIO
import spidev

from .lora_constants import *


class LoRa(object):
    def __init__(self, channel, interrupt, this_address, freq=915, tx_power=14,
                 modem_config=ModemConfig.Bw125Cr45Sf128, acks=False, crypto=None):

        self._channel = channel
        self._interrupt = interrupt

        self._mode = None
        self._cad = None
        self._freq = freq
        self._tx_power = tx_power
        self._modem_config = modem_config
        self._acks = acks

        self._this_address = this_address
        self._last_header_id = 0

        self._last_payload = None
        self.crypto = crypto

        self.cad_timeout = 1
        self.wait_packet_sent_timeout = 0.5
        self.retry_timeout = 0.5

        # Setup the module
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._interrupt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._interrupt, GPIO.RISING, callback=self._handle_interrupt)

        self.spi = spidev.SpiDev()
        self.spi.open(0, self._channel)
        self.spi.max_speed_hz = 5000000

        self._spi_write(REG_01_OP_MODE, MODE_SLEEP | LONG_RANGE_MODE)
        time.sleep(0.1)

        assert self._spi_read(REG_01_OP_MODE) == (MODE_SLEEP | LONG_RANGE_MODE), \
            "LoRa radio initialization failed"

        self._spi_write(REG_0E_FIFO_TX_BASE_ADDR, 0)
        self._spi_write(REG_0F_FIFO_RX_BASE_ADDR, 0)

        self.set_mode_idle()

        # set modem config (Bw125Cr45Sf128)
        self._spi_write(REG_1D_MODEM_CONFIG1, self._modem_config.value[0])
        self._spi_write(REG_1E_MODEM_CONFIG2, self._modem_config.value[1])
        self._spi_write(REG_26_MODEM_CONFIG3, self._modem_config.value[2])

        # set preamble length (8)
        self._spi_write(REG_20_PREAMBLE_MSB, 0)
        self._spi_write(REG_21_PREAMBLE_LSB, 8)

        # set frequency
        frf = int((self._freq * 1000000.0) / FSTEP)
        self._spi_write(REG_06_FRF_MSB, (frf >> 16) & 0xff)
        self._spi_write(REG_07_FRF_MID, (frf >> 8) & 0xff)
        self._spi_write(REG_08_FRF_LSB, frf & 0xff)

        # Set tx power
        if self._tx_power < 5:
            self._tx_power = 5
        if self._tx_power > 23:
            self._tx_power = 23

        if self._tx_power < 20:
            self._spi_write(REG_4D_PA_DAC, PA_DAC_ENABLE)
            self._tx_power -= 3
        else:
            self._spi_write(REG_4D_PA_DAC, PA_DAC_DISABLE)

        self._spi_write(REG_09_PA_CONFIG, PA_SELECT | (self._tx_power - 5))

    def on_recv(self, message):
        # This should be overridden by the user
        pass

    def sleep(self):
        if self._mode != MODE_SLEEP:
            self._spi_write(REG_01_OP_MODE, MODE_SLEEP)
            self._mode = MODE_SLEEP

    def set_mode_tx(self):
        if self._mode != MODE_TX:
            self._spi_write(REG_01_OP_MODE, MODE_TX)
            self._spi_write(REG_40_DIO_MAPPING1, 0x40)  # Interrupt on TxDone
            self._mode = MODE_TX

    def set_mode_rx(self):
        if self._mode != MODE_RXCONTINUOUS:
            self._spi_write(REG_01_OP_MODE, MODE_RXCONTINUOUS)
            self._spi_write(REG_40_DIO_MAPPING1, 0x00)  # Interrupt on RxDone
            self._mode = MODE_RXCONTINUOUS

    def set_mode_cad(self):
        self.set_mode_idle()
        time.sleep(0.1)
        self._spi_write(REG_01_OP_MODE, MODE_CAD)
        self._spi_write(REG_40_DIO_MAPPING1, 0x80)  # Interrupt on CadDone
        self._mode = MODE_CAD

    def wait_cad(self):
        # Set the radio to CAD mode to check for channel activity
        # self._cad will be True if activity was detected
        if not self.cad_timeout:
            return True

        self.set_mode_cad()

        start = time.time()
        while time.time() - start < self.cad_timeout:
            if self._mode == MODE_STDBY and self._cad:
                # Channel activity was detected, so we'll check again
                self.set_mode_cad()
            if self._mode == MODE_STDBY and not self._cad:
                return True
            time.sleep(0.1)
        return False

    def wait_packet_sent(self):
        # wait for `_handle_interrupt` to switch the mode back from MODE_TX
        start = time.time()
        while time.time() - start < self.wait_packet_sent_timeout:
            if self._mode != MODE_TX:
                return True

        return False

    def set_mode_idle(self):
        if self._mode != MODE_STDBY:
            self._spi_write(REG_01_OP_MODE, MODE_STDBY)
            self._mode = MODE_STDBY

    def send(self, data, header_to, header_id=0, header_flags=0):
        self.wait_packet_sent()
        self.set_mode_idle()
        self.wait_cad()

        header = [header_to, self._this_address, header_id, header_flags]
        if type(data) == int:
            data = [data]
        elif type(data) == bytes:
            data = [p for p in data]
        elif type(data) == str:
            data = [ord(s) for s in data]

        if self.crypto:
            data = [b for b in self._encrypt(bytes(data))]

        payload = header + data

        self._spi_write(REG_0D_FIFO_ADDR_PTR, 0)
        self._spi_write(REG_00_FIFO, payload)
        self._spi_write(REG_22_PAYLOAD_LENGTH, len(payload))

        self.set_mode_tx()
        return True

    def send_to_wait(self, data, header_to, header_flags=0, retries=3):
        self._last_header_id += 1

        for _ in range(retries + 1):
            self.send(data, header_to, header_id=self._last_header_id, header_flags=header_flags)
            self.set_mode_rx()

            if header_to == BROADCAST_ADDRESS:  # Don't wait for acks from a broadcast message
                return True

            start = time.time()
            while time.time() - start < self.retry_timeout + (self.retry_timeout * random()):
                if self._last_payload:
                    if self._last_payload.header_to == self._this_address and \
                            self._last_payload.header_flags & FLAGS_ACK and \
                            self._last_payload.header_id == self._last_header_id:

                        # We got an ACK
                        return True
        return False

    def send_ack(self, header_to, header_id):
        self.send(b'!', header_to, header_id, FLAGS_ACK)
        self.wait_packet_sent()

    def _spi_write(self, register, payload):
        if type(payload) == int:
            payload = [payload]
        elif type(payload) == bytes:
            payload = [p for p in payload]
        elif type(payload) == str:
            payload = [ord(s) for s in payload]

        self.spi.xfer([register | 0x80] + payload)

    def _spi_read(self, register, length=1):
        if length == 1:
            return self.spi.xfer([register] + [0] * length)[1]
        else:
            return self.spi.xfer([register] + [0] * length)[1:]

    def _decrypt(self, message):
        decrypted_msg = self.crypto.decrypt(message)
        msg_length = decrypted_msg[0]
        return decrypted_msg[1:msg_length + 1]

    def _encrypt(self, message):
        msg_length = len(message)
        padding = bytes(((math.ceil((msg_length + 1) / 16) * 16) - (msg_length + 1)) * [0])
        msg_bytes = bytes([msg_length]) + message + padding
        encrypted_msg = self.crypto.encrypt(msg_bytes)
        return encrypted_msg

    def _handle_interrupt(self, channel):
        irq_flags = self._spi_read(REG_12_IRQ_FLAGS)

        if self._mode == MODE_RXCONTINUOUS and (irq_flags & RX_DONE):
            packet_len = self._spi_read(REG_13_RX_NB_BYTES)
            self._spi_write(REG_0D_FIFO_ADDR_PTR, self._spi_read(REG_10_FIFO_RX_CURRENT_ADDR))

            packet = self._spi_read(REG_00_FIFO, packet_len)
            self._spi_write(REG_12_IRQ_FLAGS, 0xff)  # Clear all IRQ flags

            snr = self._spi_read(REG_19_PKT_SNR_VALUE) / 4
            rssi = self._spi_read(REG_1A_PKT_RSSI_VALUE)

            if snr < 0:
                rssi = round(snr + rssi, 2)
            else:
                rssi = round(rssi * 16 / 15, 2)

            if self._freq >= 779:
                rssi -= 157
            else:
                rssi -= 164

            if packet_len >= 4:
                header_to = packet[0]
                header_from = packet[1]
                header_id = packet[2]
                header_flags = packet[3]
                message = bytes(packet[4:]) if packet_len > 4 else b''

                if self._this_address not in [header_to, BROADCAST_ADDRESS]:
                    # Message not for us
                    return

                if self.crypto and len(message) and len(message) % 16 == 0:
                    message = self._decrypt(message)

                if self._acks and header_to == self._this_address and not header_flags & FLAGS_ACK:
                    self.send_ack(header_from, header_id)

                self.set_mode_rx()

                self._last_payload = namedtuple(
                    "Payload",
                    ['message', 'header_to', 'header_from', 'header_id', 'header_flags', 'rssi', 'snr']
                )(message, header_to, header_from, header_id, header_flags, rssi, snr)

                if not header_flags & FLAGS_ACK:
                    self.on_recv(self._last_payload)

        elif self._mode == MODE_TX and (irq_flags & TX_DONE):
            self.set_mode_idle()

        elif self._mode == MODE_CAD and (irq_flags & CAD_DONE):
            self._cad = irq_flags & CAD_DETECTED
            self.set_mode_idle()

        self._spi_write(REG_12_IRQ_FLAGS, 0xff)

    def close(self):
        GPIO.cleanup()
        self.spi.close()
