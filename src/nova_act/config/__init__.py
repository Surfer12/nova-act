# Configuration module for Nova Act
# This module handles loading and validating configuration from YAML files

from nova_act.config.config_loader import load_config, get_profile

__all__ = ["load_config", "get_profile"]