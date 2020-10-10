from src import nfc

reader = nfc.Reader()
reader.print_data(reader.get_uid())
reader.info()
