"""
API layer for AutoRESTify.

Contains:
- Application factory
- Router factory
"""

from .app_factory import create_app
from .router_factory import create_router

__all__ = [
    "create_app",
    "create_router",
]
