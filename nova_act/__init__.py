"""Nova Act package."""

__all__ = ["NovaAct", "load_config", "setup_logging"]


# Import lazily to avoid circular imports
def __getattr__(name):
    if name in __all__:
        try:
            if name == "NovaAct":
                from .nova_act import NovaAct  # Changed to relative import

                globals()[name] = NovaAct
                return NovaAct
            elif name == "load_config":
                from .main import load_config  # Changed to relative import

                globals()[name] = load_config
                return load_config
            elif name == "setup_logging":
                from .main import setup_logging  # Changed to relative import

                globals()[name] = setup_logging
                return setup_logging
        except ImportError as e:
            raise ImportError(f"Failed to import {name}: {str(e)}") from e
    raise AttributeError(f"module 'nova_act' has no attribute '{name}'")
