"""
Model2API - Application Entrypoint

This module allows running the API server directly using:

    python -m model2api.main

It uses the default application factory.
"""

import uvicorn
from model2api.api.app_factory import create_app


def run(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
) -> None:
    """
    Run the Model2API server.

    Args:
        host: Server host
        port: Server port
        reload: Enable auto-reload (development only)
    """
    app = create_app()

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
