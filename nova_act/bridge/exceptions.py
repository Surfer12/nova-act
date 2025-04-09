"""Bridge exceptions module."""


class BridgeError(Exception):
    """Base exception for bridge errors."""

    pass


class ConnectionError(BridgeError):
    """Raised when connection to bridge service fails."""

    pass


class MessageError(BridgeError):
    """Raised when message handling fails."""

    pass
