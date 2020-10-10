options = {
    "get_uid": [0xFF, 0xCA, 0x00, 0x00, 0x00],
    "firmware_version": [0xFF, 0x00, 0x48, 0x00, 0x00],
    "load_authentication_data": [0xFF, 0x82, 0x00, -1, 0x06, -1],
    "authentication": [0xFF, 0x88, 0x00, -1, -1, -1],
    "read_binary_blocks": [0xFF, 0xB0, 0x00, -1, -1],
    "update_binary_blocks": [0xFF, 0xD6, 0x00, -1, -1, -1],
    "led-control": [0xFF, 0x00, 0x40, -1, -0x04, -1, -1, -1, -1],
    "get_picc_version": [0xFF, 0x00, 0x50, 0x00, 0x00],
    "set_picc_version": [0xFF, 0x00, 0x51, -1, 0x00],
    "buzzer_sound": [0xFF, 0x00, 0x52, -1, 0x00],
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
cards = {
    "00 01": "MIFARE Classic 1K",
    "00 02": "MIFARE Classic 4K",
    "00 03": "MIFARE Ultralight",
    "00 26": "MIFARE Mini",
    "F0 04": "Topaz and Jewel",
    "F0 11": "FeliCa 212K",
    "F0 12": "FeliCa 424K"
}
