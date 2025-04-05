# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import pathlib
import sys
from platform import system
from typing import Any, Dict, List, Optional, Union

# The freedesktop_os_release function was added in Python 3.10
# For older Python versions, we'll implement a basic fallback
if sys.version_info >= (3, 10):
    from platform import freedesktop_os_release
else:

    def freedesktop_os_release():
        """Simple fallback for freedesktop_os_release on Python < 3.10."""
        try:
            with open("/etc/os-release") as f:
                info = {}
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    k, v = line.split("=", 1)
                    v = v.strip('"')
                    info[k] = v
                return info
        except (FileNotFoundError, PermissionError):
            return {}


from nova_act.types.errors import UnsupportedOperatingSystem


def decode_nested_json(obj: Union[Dict[Any, Any], List[Any], str]):
    """Decode a mixed JSON dict/list/string."""
    if isinstance(obj, dict):
        return {key: decode_nested_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decode_nested_json(value) for value in obj]
    elif isinstance(obj, str):
        try:
            return decode_nested_json(json.loads(obj))
        except json.JSONDecodeError:
            return obj
    else:
        return obj


def should_install_chromium_dependencies() -> bool:
    """Determine whether to install Chromium dependencies.

    OS specifics
    * Amazon Linux below 2023 - glibc version is too low to support the NovaAct Python SDK
    * Amazon Linux 2023 - install Chromium without dependencies

    Returns
    -------
    bool
        True if Chromium dependencies should be installed and False otherwise.

    Raises
    ------
    UnsupportedOperatingSystem
        If the underlying operating system is a version of Amazon Linux below 2023.
    """
    if system() != "Linux":
        return True

    try:
        os_release = freedesktop_os_release()
    except OSError:
        os_release = {}

    if os_release.get("NAME", "") == "Amazon Linux":
        if os_release.get("VERSION", "") == "2023":
            return False
        raise UnsupportedOperatingSystem(
            "NovaAct does not support Amazon Linux below version 2023"
        )

    return True


def get_extension_version(extension_path: str):
    """Retrieve the Extension Description in the Manifest for Version Info"""
    manifest_path = os.path.join(extension_path, "manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)
    return manifest["description"].replace(" ", "_")


def get_default_extension_path() -> str:
    """Retrieve the Extension Path"""
    path = os.path.join(
        pathlib.Path(__file__).parent.parent.resolve(), "artifacts", "chrome-mv3-prod"
    )
    if path is None:
        raise FileNotFoundError("Extension not found")
    return path
