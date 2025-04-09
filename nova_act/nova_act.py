"""Main NovaAct implementation module."""

class NovaAct:
    """Main class for the Nova ACT Framework."""
    
    def __init__(self):
        """Initialize NovaAct instance."""
        self._bridge_client = None  # Will be initialized in start()

    async def start(self):
        """Start the Nova ACT Framework."""
        from .bridge import BridgeClient
        self._bridge_client = BridgeClient()
        await self._bridge_client.connect()

    async def stop(self):
        """Stop the Nova ACT Framework."""
        if self._bridge_client:
            await self._bridge_client.close()
            self._bridge_client = None