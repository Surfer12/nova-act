"""Pytest configuration and fixtures."""
import pytest
from nova_act.nova_act import NovaAct

@pytest.fixture
async def nova_instance():
    """Provide a NovaAct instance for tests."""
    nova = NovaAct(headless=True)
    await nova.start()
    yield nova
    await nova.stop()

@pytest.fixture
def sample_html():
    """Provide sample HTML content for testing."""
    return """
    <!DOCTYPE html>
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Content</h1>
            <p>This is a test paragraph.</p>
        </body>
    </html>
    """