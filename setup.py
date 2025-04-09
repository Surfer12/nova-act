"""Setup file for nova-act package."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        package_dir={"": "src"},
        packages=find_packages(where="src", include=["nova_act*"]),
        package_data={"": ["*"]},
        include_package_data=True,
    )
