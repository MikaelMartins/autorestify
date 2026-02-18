"""
Repository layer for Model2API.

Responsible for:
- Creating tables from schema
- Performing CRUD operations
"""

from typing import Any, Dict, List, Optional, Type

from sqlalchemy.orm import Session
from sqlalchemy import inspect

from .base import Database, Base
from .dynamic_models import DynamicModelFactory


class Repository:
    """
    High-level database interaction layer.
    """

    def __init__(self, database: Database) -> None:
        self.database = database
        self.model_factory = DynamicModelFactory()

    # ----------------------------------
    # Schema / Table Management
    # ----------------------------------

    def create_tables_from_schema(
        self,
        table_name: str,
        schema: Dict[str, Any],
    ) -> None:
        """
        Generate ORM models and create tables in database.
        """

        self.model_factory.create_models_from_schema(table_name, schema)
        Base.metadata.create_all(self.database.engine)

    def table_exists(self, table_name: str) -> bool:
        inspector = inspect(self.database.engine)
        return table_name in inspector.get_table_names()

    # ----------------------------------
    # CRUD Operations
    # ----------------------------------

    def insert(
        self,
        table_name: str,
        data: Dict[str, Any],
    ) -> int:
        """
        Insert a new record.
        """

        model = self._get_model(table_name)

        with self.database.SessionLocal() as session:
            instance = model(**data)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return int(instance.id)

    def list(
        self,
        table_name: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List records from table.
        """

        model = self._get_model(table_name)

        with self.database.SessionLocal() as session:
            results = session.query(model).limit(limit).all()
            return [self._serialize(r) for r in results]

    def get(
        self,
        table_name: str,
        item_id: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Get single record by ID.
        """

        model = self._get_model(table_name)

        with self.database.SessionLocal() as session:
            instance = session.get(model, item_id)
            if not instance:
                return None
            return self._serialize(instance)

    def update(
        self,
        table_name: str,
        item_id: int,
        data: Dict[str, Any],
    ) -> bool:
        """
        Update record by ID.
        """

        model = self._get_model(table_name)

        with self.database.SessionLocal() as session:
            instance = session.get(model, item_id)
            if not instance:
                return False

            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            session.add(instance)
            session.commit()
            return True

    def delete(
        self,
        table_name: str,
        item_id: int,
    ) -> bool:
        """
        Delete record by ID.
        """

        model = self._get_model(table_name)

        with self.database.SessionLocal() as session:
            instance = session.get(model, item_id)
            if not instance:
                return False

            session.delete(instance)
            session.commit()
            return True

    # ----------------------------------
    # Internal Utilities
    # ----------------------------------

    def _get_model(self, table_name: str) -> Type[Base]:
        """
        Retrieve dynamically created model.
        """

        table_name = table_name.lower()

        if table_name not in self.model_factory._models:
            raise ValueError(f"Table '{table_name}' is not registered.")

        return self.model_factory._models[table_name]

    def _serialize(self, instance: Any) -> Dict[str, Any]:
        """
        Convert ORM instance to dictionary.
        """

        result = {}

        for column in instance.__table__.columns:
            result[column.name] = getattr(instance, column.name)

        return result
