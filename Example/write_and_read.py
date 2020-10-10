from src import nfc

reader = nfc.Reader()

reader.load_authentication_data(0x01, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
reader.authentication(0x00, 0x61, 0x01)


def write(r, position, number, data):
    while number >= 16:
        write_16(r, position, 16, data)
        number -= 16
        position += 1


def write_16(r, position, number, data):
    r.update_binary_blocks(position, number, data)


def read(r, position, number):
    result = []
    while number >= 16:
        result.append(read_16(r, position, 16))
        number -= 16
        position += 1
    return result


def read_16(r, position, number):
    return r.read_binary_blocks(position, number)

write(reader, 0x01, 0x20, [0x00 for i in range(16)])
print(read(reader, 0x01, 0x20))
