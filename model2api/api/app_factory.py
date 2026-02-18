"""
Application Factory for Model2API.

This module is responsible for creating and configuring
the FastAPI application instance.
"""

from fastapi import FastAPI

from model2api.api.router_factory import create_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """

    app = FastAPI(
        title="Model2API",
        description="Dynamic API generator from JSON models with automatic schema inference.",
        version="1.0.0",
    )

    # Include dynamic router
    router = create_router()
    app.include_router(router)

    return app
