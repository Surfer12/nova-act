"""Nova ACT main module."""

from .bridge import NovaActBridge


class NovaAct:
    """Main NovaAct class."""

    def __init__(self):
        """Initialize NovaAct."""
        self.bridge = NovaActBridge()

    async def connect(self):
        """Connect to Nova ACT bridge."""
        await self.bridge.connect()

    async def disconnect(self):
        """Disconnect from Nova ACT bridge."""
        await self.bridge.disconnect()

    @property
    def connected(self) -> bool:
        """Return True if connected to the bridge."""
        return self.bridge.connected