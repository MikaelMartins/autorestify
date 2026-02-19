"""
Dynamic model factory for AutoRESTify.

Responsible for generating SQLAlchemy models dynamically
based on inferred schema.
"""

import re
from typing import Any, Dict, Type

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


def _sanitize_name(name: str) -> str:
    """
    Normalize table/column names to safe SQL identifiers.
    """
    return re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()


class DynamicModelFactory:
    """
    Factory for creating dynamic SQLAlchemy models from schema.
    """

    def __init__(self) -> None:
        self._models: Dict[str, Type[Base]] = {}

    # ----------------------------------
    # Public API
    # ----------------------------------

    def create_models_from_schema(
        self,
        table_name: str,
        schema: Dict[str, Any],
    ) -> Dict[str, Type[Base]]:
        """
        Create main and nested models from schema.

        Returns:
            Dict of created models (table_name → model class)
        """

        main_table = _sanitize_name(table_name)

        if main_table in self._models:
            return self._models

        models_created: Dict[str, Type[Base]] = {}

        # Create main model
        main_model = self._create_main_model(main_table, schema)
        models_created[main_table] = main_model

        # Create nested models
        for field, field_type in schema.items():
            if isinstance(field_type, dict):
                child_table = f"{main_table}__{_sanitize_name(field)}"
                child_model = self._create_child_model(
                    child_table,
                    main_table,
                    field_type,
                )
                models_created[child_table] = child_model

        self._models.update(models_created)

        return models_created

    # ----------------------------------
    # Internal Methods
    # ----------------------------------

    def _create_main_model(
        self,
        table_name: str,
        schema: Dict[str, Any],
    ) -> Type[Base]:

        attrs = {
            "__tablename__": table_name,
            "id": Column(Integer, primary_key=True, autoincrement=True),
            "created_at": Column(DateTime(timezone=True), server_default=func.now()),
        }

        for field, field_type in schema.items():
            if isinstance(field_type, dict):
                continue  # nested handled separately

            column = self._map_type_to_column(field_type)
            attrs[field] = column

        model = type(f"{table_name.capitalize()}Model", (Base,), attrs)
        return model

    def _create_child_model(
        self,
        table_name: str,
        parent_table: str,
        schema: Dict[str, Any],
    ) -> Type[Base]:

        attrs = {
            "__tablename__": table_name,
            "id": Column(Integer, primary_key=True, autoincrement=True),
            "parent_id": Column(
                Integer,
                ForeignKey(f"{parent_table}.id"),
                nullable=False,
            ),
            "created_at": Column(DateTime(timezone=True), server_default=func.now()),
        }

        for field, field_type in schema.items():
            if isinstance(field_type, dict):
                attrs[field] = Column(JSON, nullable=True)
            else:
                attrs[field] = self._map_type_to_column(field_type)

        model = type(f"{table_name.capitalize()}Model", (Base,), attrs)
        return model

    def _map_type_to_column(self, field_type: str) -> Column:
        """
        Map internal type to SQLAlchemy column.
        """

        if field_type == "integer":
            return Column(Integer)

        if field_type == "float":
            return Column(Float)

        if field_type == "boolean":
            return Column(Boolean)

        if field_type == "array":
            return Column(JSON)

        if field_type == "null":
            return Column(String(255), nullable=True)

        # Default: string
        return Column(String(512))
