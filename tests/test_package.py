import importlib

import jsnake


def test_package_exposes_version() -> None:
    """The installed package should report a non-empty version string."""
    assert isinstance(jsnake.__version__, str)
    assert jsnake.__version__


def test_module_entry_point_is_importable() -> None:
    """`python -m jsnake` should resolve a valid module entry point."""
    module = importlib.import_module("jsnake.__main__")
    assert module is not None
