"""Type hints for Nova ACT."""

from typing import Any, Callable, Dict, Optional, TypeVar

# Type variables
T = TypeVar("T")

# Type aliases
JsonDict = Dict[str, Any]
MessageHandler = Callable[[JsonDict], None]
OptionalDict = Optional[Dict[str, Any]]
