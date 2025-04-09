"""ACT result types module."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ActResult:
    """Result from an ACT operation."""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[Exception] = None

    def __bool__(self) -> bool:
        """Convert to bool representation."""
        return self.success
