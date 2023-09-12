import pytest

from src.py122u.nfc import Reader


@pytest.fixture
def reader(mocker) -> Reader:
    mocker.patch("src.py122u.nfc.Reader.instantiate_reader", return_value=(None, None))
    r = Reader()
    return r


@pytest.mark.parametrize(
    "transmitted, poll_nr, period, type1",
    [
        ([0xD4, 0x60, 0xFF, 0x01, 0x10], 0xFF, 0x01, 0x10),
        ([0xD4, 0x60, 0x01, 0x02, 0x40], 0x01, 0x02, 0x40),
        ([0xD4, 0x60, 0xFE, 0x0F, 0x50], 0xFE, 0x0F, 0x50),
    ],
)
def test_in_aut_poll_commands(transmitted, poll_nr, period, type1, reader, mocker):
    mock_transmit = mocker.patch("src.py122u.nfc.Reader._PN532.transmit")

    reader.pn532.in_auto_poll(
        poll_nr,
        period,
        type1,
    )

    mock_transmit.assert_called_with(transmitted)


@pytest.mark.parametrize(
    "transmitted, poll_nr, period, type1, type2",
    [
        ([0xD4, 0x60, 0xFF, 0x01, 0x10, 0x20], 0xFF, 0x01, 0x10, 0x20),
        ([0xD4, 0x60, 0x01, 0x02, 0x40, 0x20], 0x01, 0x02, 0x40, 0x20),
        ([0xD4, 0x60, 0xFE, 0x0F, 0x50, 0x20], 0xFE, 0x0F, 0x50, 0x20),
    ],
)
def test_in_aut_poll_commands_more_types(
    transmitted, poll_nr, period, type1, type2, reader, mocker
):
    mock_transmit = mocker.patch("src.py122u.nfc.Reader._PN532.transmit")

    reader.pn532.in_auto_poll(poll_nr, period, type1, type2)

    mock_transmit.assert_called_with(transmitted)


@pytest.mark.parametrize(
    "transmitted, poll_nr, period, type1, type2, type3",
    [
        ([0xD4, 0x60, 0xFF, 0x01, 0x10, 0x20, 0x15], 0xFF, 0x01, 0x10, 0x20, 0x15),
        ([0xD4, 0x60, 0x01, 0x02, 0x40, 0x20, 0x15], 0x01, 0x02, 0x40, 0x20, 0x15),
        ([0xD4, 0x60, 0xFE, 0x0F, 0x50, 0x20, 0x15], 0xFE, 0x0F, 0x50, 0x20, 0x15),
    ],
)
def test_in_aut_poll_commands_even_more_types(
    transmitted, poll_nr, period, type1, type2, type3, reader, mocker
):
    mock_transmit = mocker.patch("src.py122u.nfc.Reader._PN532.transmit")

    reader.pn532.in_auto_poll(poll_nr, period, type1, type2, type3)

    mock_transmit.assert_called_with(transmitted)
