import smartcard.System
from smartcard.util import toHexString
from smartcard.ATR import ATR

from src import utils, option, error


class Reader:
    def __init__(self):
        """create an ACR122U object
        doc available here: http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf"""
        self.reader_name, self.connection = self.instantiate_reader()

    @staticmethod
    def instantiate_reader():
        readers = smartcard.System.readers()

        if len(readers) == 0:
            raise error.NoReader("No readers available")

        reader = readers[0]
        c = reader.createConnection()

        try:
            c.connect()
        except:
            raise error.NoCommunication(
                "The reader has been deleted and no communication is now possible. Smartcard error code : 0x7FEFFF97"
                "\nHint: try to connect a card to the reader")

        return reader, c

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
            raise error.OptionOutOfRange("Option do not exist\nHint: try to call help(nfc.Reader().command) to see all options")

        payload = utils.replace_arguments(payload, arguments)
        result = self.connection.transmit(payload)

        if len(result) == 3:
            data, sw1, sw2 = result
        else:
            data, n, sw1, sw2 = result

        if [sw1, sw2] == option.answers.get("fail"):
            raise error.InstructionFailed(f"Instruction {mode} failed")

        print(f"success: {mode}")
        if data:
            return data

        if [sw1, sw2] != option.answers.get("success"):
            return sw1, sw2

    def custom(self, payload):
        """send a custom payload to the reader

        Format:
            CLA INS P1 P2 P3 Lc Data Le"""
        result = self.connection.transmit(payload)

        if len(result) == 3:
            data, sw1, sw2 = result
        else:
            data, n, sw1, sw2 = result

        if [sw1, sw2] == option.answers.get("fail"):
            raise error.InstructionFailed(f"Payload {payload} failed")

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
