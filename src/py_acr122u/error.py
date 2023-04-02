class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoReader(Error):
    """Exception raised when no readers are plug to the computer.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class NoCommunication(Error):
    """Exception raised when the communication can't be established.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class OptionOutOfRange(Error):
    """Exception raised when you try to access an element not in the `option.options` dictionary

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class InstructionFailed(Error):
    """Exception raised when the instruction failed

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
