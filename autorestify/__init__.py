"""
AutoRESTify

Dynamic API generator from JSON models with automatic schema inference.

Public package interface.
"""

from .api.app_factory import create_app

__all__ = [
    "create_app",
]

__version__ = "1.0.2"
