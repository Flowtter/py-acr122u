# made with http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf
from smartcard.System import readers
import sys

readers = readers()

for reader in readers:
    print(reader)

if len(readers) == 0:
    sys.exit("No readers available")

reader = readers[0]
c = reader.createConnection()

try:
    c.connect()
except:
    sys.exit("The reader has been deleted and no communication is now possible. Smartcard error code : 0x7FEFFF97"
             "\nHint: try to connect a card to the reader")


# CLA INS P1 P2 P3 Lc Data Le

# with :
# The Le field (optional) indicates the maximum length of the response.
# The Lc field indicates the length of the outgoing data.

# mandatory:
# CLA INS P1 P2

options = {
    "get_uid": [0xFF, 0xCA, 0x00, 0x00, 0x00],

    "firmware_version": [0xFF, 0x00, 0x48, 0x00, 0x00],

    # key location : 0x00 ~ 0x01
    # key value : 6 bytes

    # E.g. [[0x01], [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]]
    "load_authentication_data": [0xFF, 0x82, 0x00, -1, 0x06, -1],

    # block number : 1 byte
    # key type A/B : 0x60 ~ 0x61
    # key location : 0x00 ~ 0x01

    # E.g. [[0x00], [0x61], [0x01]]
    "authentication": [0xFF, 0x88, 0x00, -1, -1, -1],

    # block number : 1 byte
    # number of Bytes to read : 1-16 bytes

    # E.g. [[0x00], [0x02]]
    "read_binary_blocks": [0xFF, 0xB0, 0x00, -1, -1],

    # block number : 1 byte
    # number of Bytes to update : 1-16 bytes
    # block data : 4-16 bytes

    # E.g. [[0x1], [0x10], [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06,
    # 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15]]
    "update_binary_blocks": [0xFF, 0xD6, 0x00, -1, -1, -1],

    # led state control : 0x00 - 0x0F
    # T1 led Duration
    # T2 led Duration
    # link to buzzer

    # E.g. [[5], [1], [1], [1], [1]]
    "led-control": [0xFF, 0x00, 0x40, -1, -0x04, -1, -1, -1, -1],

    "get_picc_version": [0xFF, 0x00, 0x50, 0x00, 0x00],

    # PICC value: 1 byte, default is 0xFF

    # E.g. [[0xFF]]
    "set_picc_version": [0xFF, 0x00, 0x51, -1, 0x00],

    # poll buzz status : 0x00 ~ 0xFF

    # E.g. [[0x00]]
    "buzzer_sound": [0xFF, 0x00, 0x52, -1, 0x00],

    # timeout parameter : 0x00 ~ 0x01 - 0xFE ~ 0xFF : (0,  5 second unit, infinite), default is 0xFF

    # E.g. [[0x01]]
    "set_timeout": [0xFF, 0x00, 0x41, -1, 0x00],
}
alias = {
    "gu": "get_uid",
    "fv": "firmware_version",
    "lad": "load_authentication_data",
    "auth": "authentication",
    "rbb": "read_binary_blocks",
    "ubb": "update_binary_blocks",

    "ld": "led-control",
    "gpv": "get_picc_version",
    "spv": "set_picc_version",
    "b": "buzzer_sound_mute",
    "st": "set_timeout",
}
answers = {
    "success": [0x90, 0x0],
    "fail": [0x63, 0x0]
}


def int_list_to_hexadecimal_list(data):
    return [hex(e) for e in data]


def int_list_to_string_list(data):
    return ''.join([chr(e) for e in data])


def replace_arguments(data, arguments):
    if not arguments:
        return data
    result = []
    j = 0
    j_max = len(arguments)
    for i in range(len(data)):
        if data[i] != -1:
            result.append(data[i])
        else:
            if j < j_max:
                for e in arguments[j]:
                    result.append(e)
                j += 1
    return result


def command(connection, mode, arguments=None):
    alias_mode = alias.get(mode)
    if not alias_mode:
        payload = options.get(mode)
    else:
        mode = alias_mode
        payload = options.get(mode)  # alias

    if not payload:
        sys.exit("Option do not exist\nHint: try to call help() to see all options")

    payload = replace_arguments(payload, arguments)
    result = connection.transmit(payload)

    if len(result) == 3:
        data, sw1, sw2 = result
    else:
        data, n, sw1, sw2 = result

    if [sw1, sw2] == answers.get("fail"):
        sys.exit(f"Instruction {mode} failed")

    print(f"success: {mode}")
    if data:
        print(f"data:\n\t{data}"
              f"\n\t{int_list_to_hexadecimal_list(data)}"
              f"\n\t{int_list_to_string_list(data)}")

    if [sw1, sw2] != answers.get("success"):
        print(f"sw1 : {sw1} {hex(sw1)}\n"
              f"sw2 : {sw2} {hex(sw2)}")
