from src.py_acr122u import nfc

reader = nfc.Reader()
reader.print_data(reader.get_uid())
reader.info()
