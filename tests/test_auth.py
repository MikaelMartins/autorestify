import pytest
from fastapi import Request
from starlette.datastructures import Headers
from starlette.requests import Request as StarletteRequest

from model2api.core.security import SecurityManager


class DummyScope(dict):
    def __init__(self):
        super().__init__()
        self["type"] = "http"
        self["headers"] = []


@pytest.mark.asyncio
async def test_default_security_allows_access():
    security = SecurityManager()

    request = StarletteRequest(DummyScope())

    user = await security.authenticate(request)

    assert user is not None

    # Should not raise
    security.authorize_read(user, "resource")
    security.authorize_write(user, "resource")
    security.authorize_delete(user, "resource")
