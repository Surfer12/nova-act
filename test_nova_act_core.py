"""Tests for core NovaAct functionality."""
from pytest import mark, fixture
from nova_act.nova_act import NovaAct

@mark.asyncio
async def test_nova_act_initialization():
    """Test NovaAct instance initialization."""
    nova = NovaAct()
    assert nova is not None

@mark.asyncio
async def test_nova_act_start_stop():
    """Test NovaAct start and stop functionality."""
    nova = NovaAct(headless=True)
    # Test initial state
    assert not hasattr(nova, '_browser'), "Browser should not exist before start"
    
    # Test start
    await nova.start()
    assert hasattr(nova, '_browser'), "Browser should exist after start"
    assert nova._browser is not None, "Browser should be initialized"
    
    # Test stop
    await nova.stop()
    assert not hasattr(nova, '_browser') or nova._browser is None, "Browser should be cleaned up after stop"

@mark.asyncio
async def test_nova_act_configuration():
    """Test NovaAct configuration options."""
    nova = NovaAct(
        headless=True,
        chrome_channel="chromium",
        screen_width=1920,
        screen_height=1080
    )
    assert nova._headless is True
    assert nova._chrome_channel == "chromium"
    assert nova._screen_width == 1920
    assert nova._screen_height == 1080