from typing import List

import smartcard.System
from smartcard.CardConnection import CardConnection
from smartcard.util import toHexString
from smartcard.ATR import ATR

from . import utils, error, option

import logging

logger = logging.getLogger(__name__)


class Reader:
    def __init__(self):
        """create an ACR122U object
        doc available here: http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf"""
        self.reader_name, self.connection = self.instantiate_reader()
        self.pn532 = self._PN532(self)

    @staticmethod
    def instantiate_reader():
        readers = smartcard.System.readers()

        logger.debug(f"Available readers: {readers}")

        if len(readers) == 0:
            raise error.NoReader("No readers available")

        reader = readers[0]
        c = reader.createConnection()

        logger.info(f"Using reader {reader}")

        return reader, c

    def connect(self):
        """connect to the card
        only works if a card is on the reader"""
        try:
            self.connection.connect()
            logger.debug("Reader connected")
        except:
            raise error.NoCommunication(
                "The reader has been deleted and no communication is now possible. Smartcard error code : 0x7FEFFF97"
                "\nHint: try to connect a card to the reader")

    def command(self, mode, arguments=None):
        """send a payload to the reader

        Format:
            CLA INS P1 P2 P3 Lc Data Le

        The Le field (optional) indicates the maximum length of the response.
        The Lc field indicates the length of the outgoing data.

        Mandatory:
            CLA INS P1 P2

        Attributes:
            mode: key value of option.options or option.alias
            arguments: replace `-1` in the payload by arguments

        Returns:
            return the data or sw1 sw2 depending on the request"""
        mode = option.alias.get(mode) or mode
        payload = option.options.get(mode)

        if not payload:
            raise error.OptionOutOfRange(
                "Option do not exist\nHint: try to call help(nfc.Reader().command) to see all options")

        payload = utils.replace_arguments(payload, arguments)
        logger.debug(f"Transmitting {payload}")
        result = self.connection.transmit(payload, protocol=CardConnection.T1_protocol)

        if len(result) == 3:
            data, sw1, sw2 = result
        else:
            data, n, sw1, sw2 = result

        if [sw1, sw2] == option.answers.get("fail"):
            raise error.InstructionFailed(f"Instruction {mode} failed")

        logger.debug(f"Success: {mode}, result: {result}")

        if data:
            return data

        if [sw1, sw2] != option.answers.get("success"):
            return sw1, sw2

    def custom(self, payload):
        """send a custom payload to the reader

        Format:
            CLA INS P1 P2 P3 Lc Data Le"""
        logger.debug(f"Transmitting {payload}")
        result = self.connection.transmit(payload)

        if len(result) == 3:
            data, sw1, sw2 = result
        else:
            data, n, sw1, sw2 = result

        if [sw1, sw2] == option.answers.get("fail"):
            raise error.InstructionFailed(f"Payload {payload} failed")

        logger.debug(f"Success transmitting payload: {payload}")

    def get_uid(self):
        """get the uid of the card"""
        return self.command("get_uid")

    def firmware_version(self):
        """get the firmware version of the reader"""
        return self.command("firmware_version")

    def load_authentication_data(self, key_location, key_value):
        """load the authentication key

        Attributes:
            key location : 0x00 ~ 0x01
            key value : 6 bytes

        Example:
            E.g. 0x01, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]"""
        self.command("load_authentication_data", [key_location, key_value])

    def authentication(self, bloc_number, key_type, key_location):
        """authentication with the key in `load_authentication_data`

        Attributes:
            block number : 1 byte
            key type A/B : 0x60 ~ 0x61
            key location : 0x00 ~ 0x01

        Example:
            E.g. 0x00, 0x61, 0x01"""
        self.command("authentication", [bloc_number, key_type, key_location])

    def read_binary_blocks(self, block_number, number_of_byte_to_read):
        """read n bytes in the card at the block_number index

        Attributes:
            block number : 1 byte
            number of Bytes to read : 1

        Example:
            E.g. 0x00, 0x02"""
        return self.command("read_binary_blocks", [block_number, number_of_byte_to_read])

    def update_binary_blocks(self, block_number, number_of_byte_to_update, block_data):
        """update n bytes in the card with block_data at the block_number index

        Attributes:
            block number : 1 byte
            number of Bytes to update : 1-16 bytes
            block data : 4-16 bytes

        Examples:
            0x01, 0x10, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05
            0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15]"""
        self.command("update_binary_blocks", [block_number, number_of_byte_to_update, block_data])

    def led_control(self, led_state, t1, t2, number_of_repetition, link_to_buzzer):
        """control led state

        Attributes:
            led state control : 0x00 - 0x0F
            T1 led Duration
            T2 led Duration
            number of repetition
            link to buzzer

        Example:
            0x05, 0x01, 0x01, 0x01, 0x01"""
        self.command("led_control", [led_state, t1, t2, number_of_repetition, link_to_buzzer])

    def get_picc_version(self):
        """get the PICC version of the reader"""
        return self.command("get_picc_version")

    def set_picc_version(self, picc_value):
        """set the PICC version of the reader

        Attributes:
            PICC value: 1 byte, default is 0xFF

        Example:
            0xFF"""
        self.command("set_picc_version", [picc_value])

    def buzzer_sound(self, poll_buzzer_status):
        """set the buzzer sound state

        Attributes:
            poll buzz status : 0x00 ~ 0xFF

        Example:
            0x00"""
        self.command("buzzer_sound", [poll_buzzer_status])

    def set_timeout(self, timeout_parameter):
        """set the timeout of the reader

        Attributes:
            timeout parameter : 0x00 ~ 0x01 - 0xFE ~ 0xFF : (0,  5 second unit, infinite), default is 0xFF

        Example:
            0x01"""
        self.command("set_timeout", [timeout_parameter])

    def direct_transmit(self, payload: List[int]):
        """send the payload to the tag or reader.
        using this you can send messages directly to the PN532 chip
        doc available here: https://www.nxp.com/docs/en/user-guide/141520.pdf

        Attributes:
            payload: the payload to send to the PN532 chip

        Example:
            [0xd4, 0x60, 0xFF, 0x02, 0x10]
        """
        return self.command("direct_transmit", [len(payload), payload])

    def set_auto_polling(self, enabled: bool):
        """enable or disable Auto PICC Polling

        Attributes:
            enabled: True to enable, False to disable

        """
        self.set_picc_bit(7, enabled)

    def set_picc_bit(self, bit: int, value: bool):
        """set a PICC bit to update the PICC operating parameter as described in section 6.5
        of API-ACR122U-2.02.pdf

        Attributes:
            bit: the bit to set
            value: True for 1, False for 0
        """
        if bit < 0 or bit > 7:
            raise error.BitOutOfRange(f"Bit {bit} is not in the picc operating parameter")

        picc = self.get_picc_version()[1]
        if value:
            picc |= 1 << bit
        else:
            picc &= ~ (1 << bit)
        self.set_picc_version(picc)

    def mute_buzzer(self):
        """mute the buzzer for when a card is scanned"""
        self.buzzer_sound(0x00)

    def unmute_buzzer(self):
        """unmute the buzzer for when a card is scanned"""
        self.buzzer_sound(0xFF)

    def reset_lights(self):
        """turn the red and green LED off"""
        self.led_control(0b00001100, 0x00, 0x00, 0x00, 0x00)

    def info(self):
        """print the type of the card on the reader"""
        atr = ATR(self.connection.getATR())
        historical_byte = toHexString(atr.getHistoricalBytes(), 0)
        print(historical_byte)
        print(historical_byte[-17:-12])
        card_name = historical_byte[-17:-12]
        name = option.cards.get(card_name, "")
        print(f"Card Name: {name}\n\tT0 {atr.isT0Supported()}\n\tT1 {atr.isT1Supported()}\n\tT1 {atr.isT15Supported()}")

    @staticmethod
    def print_data(data):
        print(f"data:\n\t{data}"
              f"\n\t{utils.int_list_to_hexadecimal_list(data)}"
              f"\n\t{utils.int_list_to_string_list(data)}")

    @staticmethod
    def print_sw1_sw2(sw1, sw2):
        print(f"sw1 : {sw1} {hex(sw1)}\n"
              f"sw2 : {sw2} {hex(sw2)}")

    class _PN532:
        """the PN532 chip inside the ACR122U
        Methods in the class can be used to communicate with the chip
        see docs at: https://www.nxp.com/docs/en/user-guide/141520.pdf
        """

        def __init__(self, acr122u):
            """create a PN532 object

            Attributes:
                acr122u: the reader used to communicate with the chip (i.e. the reader the chip is in)
            """
            self.acr122u: Reader = acr122u

        def transmit(self, payload: List[int]):
            """send a payload to the chip

            Attributes:
                payload: the payload to send

            Returns:
                the response from the chip
            """
            logger.debug(f"Transmitting payload {payload} to PN532")
            return self.acr122u.direct_transmit(payload)

        def command(self, mode, arguments=None):
            """send a command to the chip

            Attributes:
                mode: key value of option.pn532_options
                arguments: replace `-1` in the payload by arguments

            Returns:
                the response from the chip
            """
            payload = option.pn532_options.get(mode)

            if not payload:
                raise error.OptionOutOfRange(
                    "Option do not exist\nHint: try to call help(nfc.Reader().command) to see all options")

            payload = utils.replace_arguments(payload, arguments)
            result = self.transmit(payload)

            return result

        def in_auto_poll(self, poll_nr: int, period: int, type1: int, *types):
            """
            this command is used to poll card(s) / target(s) of specified Type present in the RF field.
            docs: https://www.nxp.com/docs/en/user-guide/141520.pdf section 7.3.13

            Attributes:
                poll_nr -  specifies the number of polling (one polling is a polling for each Type j)
                    0x01: 0xFE:1 up to 254 polling
                    0xFF: Endless polling
                period - (0x01 – 0x0F) indicates the polling period in units of 150 ms
                type1 - indicates the mandatory target type to be polled at the 1st time
                types -  indicate the optional target types to be polled at the 2nd up to the Nth time (N ≤ 15).


            Returns:
                the response from the chip
            """
            arguments = [poll_nr, period, type1] + list(types)

            data = self.command("in_auto_poll", arguments)
            return data
