"""
Schema inference module for Autorestify.

Responsible for generating a unified schema from
a list of JSON-like documents.
"""

from typing import Any, Dict, List
from collections import defaultdict

from .engine import Engine


class SchemaInferer:
    """
    Infer a consistent schema from a list of documents.
    """

    def __init__(self, engine: Engine | None = None) -> None:
        self.engine = engine or Engine()

    # ----------------------------------
    # Public API
    # ----------------------------------

    def infer(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Infer schema from list of documents.
        """

        if not documents:
            return {}

        field_types: Dict[str, List[str]] = defaultdict(list)

        for doc in documents:
            if not isinstance(doc, dict):
                continue

            for field, value in doc.items():
                detected = self.engine.detect_type(value)
                field_types[field].append(detected)

        return self._resolve_schema(field_types, documents)

    # ----------------------------------
    # Private Methods
    # ----------------------------------

    def _resolve_schema(
        self,
        field_types: Dict[str, List[str]],
        documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        schema: Dict[str, Any] = {}

        for field, types in field_types.items():
            unique_types = set(types)

            # -------------------------
            # Nested Object Handling
            # -------------------------
            if "object" in unique_types:
                nested_docs = [
                    doc.get(field)
                    for doc in documents
                    if isinstance(doc.get(field), dict)
                ]
                schema[field] = self.infer(nested_docs)
                continue

            # -------------------------
            # Type Conflict Resolution
            # -------------------------
            schema[field] = self._merge_scalar_types(unique_types)

        return schema

    # ----------------------------------
    # Type Merging Logic
    # ----------------------------------

    def _merge_scalar_types(self, types: set[str]) -> str:
        """
        Resolve scalar type conflicts.
        """

        # Only one type
        if len(types) == 1:
            return next(iter(types))

        numeric_types = {"integer", "float"}

        # Numeric promotion: integer + float → float
        if types.issubset(numeric_types):
            return "float"

        # Boolean mixed with integer (common JSON ambiguity)
        if types == {"boolean", "integer"}:
            return "integer"

        # Everything else → fallback to string
        return "string"
