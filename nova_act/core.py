"""Core NovaAct implementation module."""

class NovaAct:
    """Core NovaAct class for browser automation."""
    
    def __init__(self, headless: bool = False):
        """Initialize NovaAct instance.
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.headless = headless

    async def start(self):
        """Start the NovaAct instance."""
        pass

    async def stop(self):
        """Stop the NovaAct instance."""
        pass