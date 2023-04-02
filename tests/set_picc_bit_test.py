import pytest

from py_acr122u import error
from py_acr122u.nfc import Reader


@pytest.mark.parametrize("bit", [0, 1, 2, 3, 4, 5, 6, 7])
def test_picc_bit_range_pass(bit, mocker):
    mocker.patch("py_acr122u.nfc.Reader.instantiate_reader", return_value=(None, None))
    mocker.patch("py_acr122u.nfc.Reader.get_picc_version", return_value=(144, 255))
    mocker.patch("py_acr122u.nfc.Reader.set_picc_version")
    r = Reader()

    r.set_picc_bit(bit, False)
    r.set_picc_bit(bit, True)


@pytest.mark.parametrize("bit", [-2, -1, 8, 9, 10])
def test_picc_bit_range_fail(bit, mocker):
    mocker.patch("py_acr122u.nfc.Reader.instantiate_reader", return_value=(None, None))
    mocker.patch("py_acr122u.nfc.Reader.get_picc_version", return_value=(144, 255))
    mocker.patch("py_acr122u.nfc.Reader.set_picc_version")
    r = Reader()

    with pytest.raises(error.BitOutOfRange):
        r.set_picc_bit(bit, False)
    with pytest.raises(error.BitOutOfRange):
        r.set_picc_bit(bit, True)


@pytest.mark.parametrize("old_picc, bit, value, new_picc", [
    (0b00000000, 0, True, 0b00000001),
    (0b00000000, 0, False, 0b00000000),
    (0b00000000, 1, True, 0b00000010),
    (0b00000000, 1, False, 0b00000000),
    (0b11111111, 0, True, 0b11111111),
    (0b11111111, 0, False, 0b11111110),
    (0b11111111, 1, True, 0b11111111),
    (0b11111111, 1, False, 0b11111101),
])
def test_picc_bit_set_bit(old_picc, bit, value, new_picc, mocker):
    mocker.patch("py_acr122u.nfc.Reader.instantiate_reader", return_value=(None, None))
    mocker.patch("py_acr122u.nfc.Reader.get_picc_version", return_value=(144, old_picc))
    mock_set_picc = mocker.patch("py_acr122u.nfc.Reader.set_picc_version")
    r = Reader()

    r.set_picc_bit(bit, value)

    mock_set_picc.assert_called_with(new_picc)
