"""Tests for verifying project structure and component interactions."""

import os
import unittest
from importlib import import_module
from typing import Any


class TestProjectStructure(unittest.TestCase):
    """Test cases for verifying project structure and component availability."""

    def test_core_components_exist(self) -> None:
        """Test that all core components are present in the project."""
        core_components = [
            "nova_act.nova_act",
            "nova_act.bridge.client",
            "nova_act.bridge.server",
            "nova_act.impl.backend",
            "nova_act.impl.playwright",
            "nova_act.impl.protocol",
            "nova_act.types.act_errors",
            "nova_act.types.act_metadata",
            "nova_act.types.act_result",
            "nova_act.util.jsonschema",
            "nova_act.util.logging",
        ]

        for component in core_components:
            try:
                import_module(component)
            except ImportError as e:
                self.fail(f"Failed to import {component}: {str(e)}")

    def test_project_structure(self) -> None:
        """Test that the project directory structure matches expectations."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        required_dirs = [
            os.path.join(base_dir, "src", "nova_act"),
            os.path.join(base_dir, "src", "nova_act", "bridge"),
            os.path.join(base_dir, "src", "nova_act", "cli"),
            os.path.join(base_dir, "src", "nova_act", "impl"),
            os.path.join(base_dir, "src", "nova_act", "samples"),
            os.path.join(base_dir, "src", "nova_act", "types"),
            os.path.join(base_dir, "src", "nova_act", "util"),
            os.path.join(base_dir, "tests"),
            os.path.join(base_dir, "docs"),
        ]

        for directory in required_dirs:
            self.assertTrue(
                os.path.isdir(directory), f"Required directory {directory} does not exist"
            )

    def test_core_dependencies_importable(self) -> None:
        """Test that all core dependencies can be imported."""
        core_deps = [
            "playwright",
            "pydantic",
            "websockets",
            "cryptography",
            "pandas",
            "numpy",
        ]

        for dep in core_deps:
            try:
                import_module(dep)
            except ImportError as e:
                self.fail(f"Failed to import core dependency {dep}: {str(e)}")

    def test_development_dependencies_importable(self) -> None:
        """Test that all development dependencies can be imported."""
        dev_deps = [
            "pytest",
            "ruff",
            "mypy",
        ]

        for dep in dev_deps:
            try:
                import_module(dep)
            except ImportError as e:
                self.fail(f"Failed to import development dependency {dep}: {str(e)}")


if __name__ == "__main__":
    unittest.main()
