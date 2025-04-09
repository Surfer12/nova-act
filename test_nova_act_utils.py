"""Tests for NovaAct utility functions."""
import pytest
from nova_act.nova_act import NovaAct
from nova_act.util.jsonschema import (
    BOOL_SCHEMA,
    validate_schema
)

def test_schema_validation():
    """Test JSON schema validation."""
    # Test boolean schema
    assert validate_schema(True, BOOL_SCHEMA)
    assert validate_schema(False, BOOL_SCHEMA)
    assert not validate_schema("true", BOOL_SCHEMA)
    assert not validate_schema(1, BOOL_SCHEMA)

@pytest.mark.asyncio
async def test_error_handling_timeout():
    """Test timeout handling."""
    nova = NovaAct(headless=True)
    await nova.start()
    try:
        with pytest.raises(Exception):
            # Set a very short timeout to force error
            await nova.act(
                "Find an element that doesn't exist",
                timeout=0.1
            )
    finally:
        await nova.stop()