"""Tests for CLI functionality."""

import pytest
import sys
import json
from unittest.mock import patch, MagicMock
from io import StringIO


@pytest.fixture
def mock_nova_act_class():
    """Create a mock NovaAct class."""
    with patch("nova_act.cli.main.NovaAct") as mock_class:
        # Setup the instance that will be returned
        mock_instance = MagicMock()
        mock_instance.start = MagicMock()
        mock_instance.stop = MagicMock()
        mock_instance.act = MagicMock()

        # Setup the class to return our instance
        mock_class.return_value = mock_instance

        yield mock_class, mock_instance


def test_cli_help():
    """Test CLI help output."""
    from nova_act.cli.main import main

    # Capture stdout
    saved_stdout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out

        # Run with help flag
        with patch.object(sys, "argv", ["nova-act", "--help"]):
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0

        output = out.getvalue()
        # Check for expected help text
        assert "usage:" in output
        assert "--headless" in output
        assert "Chrome options" in output

    finally:
        sys.stdout = saved_stdout


def test_cli_version():
    """Test CLI version output."""
    from nova_act.cli.main import main

    # Capture stdout
    saved_stdout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out

        # Run with version flag
        with patch.object(sys, "argv", ["nova-act", "--version"]):
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0

        output = out.getvalue()
        # Check for version output format
        assert "nova-act" in output.lower()
        assert "." in output  # Version number should contain dots

    finally:
        sys.stdout = saved_stdout


def test_cli_basic_command(mock_nova_act_class):
    """Test basic CLI command execution."""
    from nova_act.cli.main import main

    mock_class, mock_instance = mock_nova_act_class
    mock_result = MagicMock()
    mock_result.raw_response = "Test response"
    mock_instance.act.return_value = mock_result

    # Run with basic command
    with patch.object(sys, "argv", ["nova-act", "navigate to example.com"]):
        main()

    # Verify NovaAct was initialized correctly
    mock_class.assert_called_once()

    # Verify start, act, and stop were called
    mock_instance.start.assert_called_once()
    mock_instance.act.assert_called_once_with("navigate to example.com")
    mock_instance.stop.assert_called_once()


def test_cli_with_options(mock_nova_act_class):
    """Test CLI with various options."""
    from nova_act.cli.main import main

    mock_class, mock_instance = mock_nova_act_class
    mock_result = MagicMock()
    mock_result.raw_response = "Test response"
    mock_instance.act.return_value = mock_result

    # Run with multiple options
    with patch.object(
        sys,
        "argv",
        [
            "nova-act",
            "--headless",
            "--chrome-channel=chromium",
            "--screen-width=1280",
            "--screen-height=720",
            "navigate to example.com",
        ],
    ):
        main()

    # Verify NovaAct was initialized with correct parameters
    mock_class.assert_called_once_with(
        headless=True, chrome_channel="chromium", screen_width=1280, screen_height=720
    )

    # Verify start, act, and stop were called
    mock_instance.start.assert_called_once()
    mock_instance.act.assert_called_once()
    mock_instance.stop.assert_called_once()


def test_cli_output_json(mock_nova_act_class):
    """Test CLI JSON output format."""
    from nova_act.cli.main import main

    mock_class, mock_instance = mock_nova_act_class

    # Create a more complex result
    mock_result = MagicMock()
    mock_result.raw_response = "Test response"
    mock_result.parsed_response = {
        "title": "Example Domain",
        "url": "https://example.com",
    }
    mock_result.matches_schema = True
    mock_result.metadata = {"start_time": 1234, "end_time": 1235, "elapsed_time": 1}
    mock_instance.act.return_value = mock_result

    # Capture stdout
    saved_stdout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out

        # Run with JSON output flag
        with patch.object(
            sys, "argv", ["nova-act", "--output=json", "what is the page title"]
        ):
            main()

        output = out.getvalue()

        # Should be valid JSON
        output_data = json.loads(output)
        assert "raw_response" in output_data
        assert output_data["raw_response"] == "Test response"

    finally:
        sys.stdout = saved_stdout


def test_cli_with_timeout(mock_nova_act_class):
    """Test CLI with timeout option."""
    from nova_act.cli.main import main

    mock_class, mock_instance = mock_nova_act_class
    mock_result = MagicMock()
    mock_result.raw_response = "Test response"
    mock_instance.act.return_value = mock_result

    # Run with timeout option
    with patch.object(
        sys, "argv", ["nova-act", "--timeout=30", "navigate to example.com"]
    ):
        main()

    # Verify act was called with timeout
    mock_instance.act.assert_called_once_with("navigate to example.com", timeout=30)


def test_cli_with_schema(mock_nova_act_class):
    """Test CLI with schema option."""
    from nova_act.cli.main import main

    mock_class, mock_instance = mock_nova_act_class
    mock_result = MagicMock()
    mock_result.raw_response = "Test response"
    mock_instance.act.return_value = mock_result

    schema_str = '{"type": "boolean"}'

    # Run with schema option
    with patch.object(
        sys, "argv", ["nova-act", f"--schema={schema_str}", "is the sky blue"]
    ):
        main()

    # Verify act was called with schema
    mock_instance.act.assert_called_once_with(
        "is the sky blue", schema={"type": "boolean"}
    )


def test_cli_error_handling(mock_nova_act_class):
    """Test CLI error handling."""
    from nova_act.cli.main import main

    mock_class, mock_instance = mock_nova_act_class
    mock_instance.act.side_effect = Exception("Test error")

    # Run command that will cause an error
    with patch.object(sys, "argv", ["nova-act", "navigate to example.com"]):
        with pytest.raises(Exception):
            main()

    # Verify stop was still called (cleanup)
    mock_instance.stop.assert_called_once()


def test_cli_async_mode():
    """Test CLI in async mode."""
    from nova_act.cli.async_main import main as async_main

    with patch("nova_act.cli.async_main.NovaAct") as mock_class:
        # Setup the instance that will be returned
        mock_instance = MagicMock()
        mock_instance.start = MagicMock()
        mock_instance.stop = MagicMock()
        mock_instance.act = MagicMock()

        # Setup the class to return our instance
        mock_class.return_value = mock_instance

        # Run with async flag
        with patch.object(
            sys, "argv", ["nova-act", "--async", "navigate to example.com"]
        ):
            async_main()

        # Verify NovaAct was initialized
        mock_class.assert_called_once()

        # Verify async methods were called
        mock_instance.start.assert_called_once()
        mock_instance.act.assert_called_once()
        mock_instance.stop.assert_called_once()
