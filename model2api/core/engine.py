"""
Engine module for Model2API.

Responsible for deterministic type detection based on Python types.
No AI dependencies.
"""

from typing import Any


class Engine:
    """
    Deterministic type inference engine.

    Maps Python values to internal schema types.
    """

    def detect_type(self, value: Any) -> str:
        """
        Detect internal type label from a Python value.

        Supported types:
            - string
            - integer
            - float
            - boolean
            - object
            - null
        """

        if value is None:
            return "null"

        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, int) and not isinstance(value, bool):
            return "integer"

        if isinstance(value, float):
            return "float"

        if isinstance(value, dict):
            return "object"

        if isinstance(value, list):
            return "array"

        return "string"
