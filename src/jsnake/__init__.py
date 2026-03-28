"""JSNAKE package metadata."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("jsnake")
except PackageNotFoundError:
    __version__ = "0.1.6"

__all__ = ["__version__"]
