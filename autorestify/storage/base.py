"""
Database base configuration for Autorestify.

Responsible for:
- SQLAlchemy engine creation
- Session management
- Declarative Base
- Proper SQLite in-memory handling for tests
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool


Base = declarative_base()


class Database:
    """
    Database configuration and session management.
    """

    def __init__(
        self,
        database_url: str = "sqlite:///./autorestify.db",
        echo: bool = False,
    ) -> None:
        """
        Initialize database engine and session factory.

        Args:
            database_url: Database connection string
            echo: Enable SQLAlchemy query logging
        """

        # Special handling for SQLite in-memory databases
        if database_url.startswith("sqlite") and ":memory:" in database_url:
            self.engine: Engine = create_engine(
                database_url,
                echo=echo,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                future=True,
            )
        else:
            self.engine: Engine = create_engine(
                database_url,
                echo=echo,
                future=True,
            )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    # ----------------------------------
    # Public Methods
    # ----------------------------------

    def create_all(self) -> None:
        """
        Create all registered tables.
        """
        Base.metadata.create_all(self.engine)

    def drop_all(self) -> None:
        """
        Drop all tables (useful for testing).
        """
        Base.metadata.drop_all(self.engine)

    def get_session(self) -> Generator:
        """
        Provide a transactional session scope.
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
