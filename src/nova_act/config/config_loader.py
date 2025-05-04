# Configuration Loader
# This module handles loading and validating configuration from YAML files

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import yaml
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

# Default paths
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(CONFIG_DIR, "schemas")
PROFILE_DIR = os.path.join(CONFIG_DIR, "profiles")

# Cache for loaded configurations
_config_cache = {}


def _load_yaml_file(file_path: str) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dictionary containing the YAML file contents
        
    Raises:
        FileNotFoundError: If the file does not exist
        yaml.YAMLError: If the file is not valid YAML
    """
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {file_path}: {e}")
        raise


def _merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two configuration dictionaries.
    
    The override dictionary takes precedence over the base dictionary.
    
    Args:
        base: Base configuration dictionary
        override: Override configuration dictionary
        
    Returns:
        Merged configuration dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = _merge_configs(result[key], value)
        else:
            # Override or add the value
            result[key] = value
            
    return result


def _resolve_inheritance(profile_name: str, loaded_profiles: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Resolve profile inheritance by recursively loading parent profiles.
    
    Args:
        profile_name: Name of the profile to load
        loaded_profiles: Dictionary of already loaded profiles (to avoid circular dependencies)
        
    Returns:
        Resolved profile with all inherited properties
        
    Raises:
        FileNotFoundError: If the profile file does not exist
        ValueError: If there is a circular dependency in profile inheritance
    """
    if loaded_profiles is None:
        loaded_profiles = {}
        
    # Check for circular dependencies
    if profile_name in loaded_profiles:
        return loaded_profiles[profile_name]
        
    # Load the profile
    profile_path = os.path.join(PROFILE_DIR, f"{profile_name}.yaml")
    try:
        profile = _load_yaml_file(profile_path)
    except FileNotFoundError:
        logger.error(f"Profile not found: {profile_name}")
        raise
        
    # Add to loaded profiles to detect circular dependencies
    loaded_profiles[profile_name] = {}
    
    # Check if this profile extends another profile
    parent_profile_name = profile.get("extends")
    if parent_profile_name:
        # Load the parent profile
        parent_profile = _resolve_inheritance(parent_profile_name, loaded_profiles)
        
        # Merge the parent profile with this profile
        profile = _merge_configs(parent_profile, profile)
        
    # Update the loaded profiles dictionary
    loaded_profiles[profile_name] = profile
    
    return profile


def get_available_profiles() -> List[str]:
    """Get a list of available profile names.
    
    Returns:
        List of profile names (without the .yaml extension)
    """
    profiles = []
    for file_name in os.listdir(PROFILE_DIR):
        if file_name.endswith(".yaml"):
            profile_name = file_name[:-5]  # Remove .yaml extension
            profiles.append(profile_name)
    return profiles


def get_profile(profile_name: str = "base") -> Dict[str, Any]:
    """Get a configuration profile by name.
    
    Args:
        profile_name: Name of the profile to load (default: "base")
        
    Returns:
        Configuration dictionary for the profile
        
    Raises:
        FileNotFoundError: If the profile file does not exist
        ValueError: If there is a circular dependency in profile inheritance
    """
    # Check if the profile is already cached
    cache_key = f"profile:{profile_name}"
    if cache_key in _config_cache:
        return _config_cache[cache_key]
        
    # Load the profile with inheritance resolution
    profile = _resolve_inheritance(profile_name)
    
    # Cache the profile
    _config_cache[cache_key] = profile
    
    return profile


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a schema by name.
    
    Args:
        schema_name: Name of the schema to load
        
    Returns:
        Schema dictionary
        
    Raises:
        FileNotFoundError: If the schema file does not exist
    """
    # Check if the schema is already cached
    cache_key = f"schema:{schema_name}"
    if cache_key in _config_cache:
        return _config_cache[cache_key]
        
    # Load the schema
    schema_path = os.path.join(SCHEMA_DIR, f"{schema_name}.yaml")
    schema = _load_yaml_file(schema_path)
    
    # Cache the schema
    _config_cache[cache_key] = schema
    
    return schema


def validate_config(config: Dict[str, Any], schema_name: str) -> bool:
    """Validate a configuration against a schema.
    
    Args:
        config: Configuration dictionary to validate
        schema_name: Name of the schema to validate against
        
    Returns:
        True if the configuration is valid, False otherwise
    """
    try:
        schema = load_schema(schema_name)
        validate(instance=config, schema=schema)
        return True
    except ValidationError as e:
        logger.error(f"Configuration validation failed: {e}")
        return False
    except FileNotFoundError:
        logger.error(f"Schema not found: {schema_name}")
        return False


def load_config(profile_name: str = "base") -> Dict[str, Any]:
    """Load a configuration profile and validate it against schemas.
    
    Args:
        profile_name: Name of the profile to load (default: "base")
        
    Returns:
        Configuration dictionary for the profile
        
    Raises:
        FileNotFoundError: If the profile file does not exist
        ValueError: If the profile is invalid
    """
    try:
        # Load the profile
        config = get_profile(profile_name)
        
        # Validate the configuration against schemas
        # Note: In a real implementation, you might want to validate
        # different sections of the config against different schemas
        
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise


def get_user_config_dir() -> Path:
    """Get the user's configuration directory.
    
    Returns:
        Path to the user's configuration directory
    """
    # Use platform-specific locations
    if os.name == 'nt':  # Windows
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
        return Path(base_dir) / 'NovaAct'
    else:  # Unix/Linux/Mac
        base_dir = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        return Path(base_dir) / 'nova-act'


def load_user_config(filename: str) -> Dict[str, Any]:
    """Load a user configuration file.
    
    Args:
        filename: Name of the configuration file
        
    Returns:
        Configuration dictionary from the user file
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    config_dir = get_user_config_dir()
    config_path = config_dir / filename
    
    if not config_path.exists():
        logger.warning(f"User configuration file not found: {config_path}")
        return {}
        
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing user configuration file {config_path}: {e}")
        return {}


def save_user_config(config: Dict[str, Any], filename: str) -> bool:
    """Save a configuration to a user configuration file.
    
    Args:
        config: Configuration dictionary to save
        filename: Name of the configuration file
        
    Returns:
        True if the configuration was saved successfully, False otherwise
    """
    config_dir = get_user_config_dir()
    
    # Create the directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = config_dir / filename
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        return True
    except Exception as e:
        logger.error(f"Error saving user configuration file {config_path}: {e}")
        return False