"""
Security abstractions for Model2API.

Defines pluggable authentication and authorization system.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


# =========================================================
# Auth Provider Interface
# =========================================================

class AuthProvider(ABC):
    """
    Base authentication provider interface.
    """

    @abstractmethod
    async def authenticate(self, request: Any) -> Optional[Any]:
        """
        Authenticate request and return user object.

        Return:
            - User object if authenticated
            - None if authentication fails
        """
        pass


# =========================================================
# Access Policy Interface
# =========================================================

class AccessPolicy(ABC):
    """
    Authorization policy interface.
    """

    @abstractmethod
    def can_read(self, user: Any, resource: str) -> bool:
        pass

    @abstractmethod
    def can_write(self, user: Any, resource: str) -> bool:
        pass

    @abstractmethod
    def can_delete(self, user: Any, resource: str) -> bool:
        pass


# =========================================================
# Default Implementations
# =========================================================

class NoAuthProvider(AuthProvider):
    """
    Default authentication provider (no security).
    """

    async def authenticate(self, request: Any) -> Optional[Any]:
        return {"anonymous": True}


class AllowAllPolicy(AccessPolicy):
    """
    Default policy that allows everything.
    """

    def can_read(self, user: Any, resource: str) -> bool:
        return True

    def can_write(self, user: Any, resource: str) -> bool:
        return True

    def can_delete(self, user: Any, resource: str) -> bool:
        return True


# =========================================================
# Security Manager
# =========================================================

class SecurityManager:
    """
    Central security orchestrator.
    """

    def __init__(
        self,
        auth_provider: Optional[AuthProvider] = None,
        access_policy: Optional[AccessPolicy] = None,
    ) -> None:

        self.auth_provider = auth_provider or NoAuthProvider()
        self.access_policy = access_policy or AllowAllPolicy()

    async def authenticate(self, request: Any) -> Any:
        user = await self.auth_provider.authenticate(request)
        if user is None:
            raise PermissionError("Authentication failed")
        return user

    def authorize_read(self, user: Any, resource: str) -> None:
        if not self.access_policy.can_read(user, resource):
            raise PermissionError("Read access denied")

    def authorize_write(self, user: Any, resource: str) -> None:
        if not self.access_policy.can_write(user, resource):
            raise PermissionError("Write access denied")

    def authorize_delete(self, user: Any, resource: str) -> None:
        if not self.access_policy.can_delete(user, resource):
            raise PermissionError("Delete access denied")
