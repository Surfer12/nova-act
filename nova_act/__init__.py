"""Nova Act package."""

__all__ = ["load_config", "setup_logging"]


# Import lazily to avoid circular imports
def __getattr__(name):
    if name in __all__:
        from nova_act.main import load_config, setup_logging

        return globals()[name]
    raise AttributeError(f"module 'nova_act' has no attribute '{name}'")
