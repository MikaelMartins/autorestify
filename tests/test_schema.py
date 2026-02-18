import pytest

from model2api.core.schema_inference import SchemaInferer


def test_infer_simple_schema():
    inferer = SchemaInferer()

    documents = [
        {"name": "Ana", "age": 30},
        {"name": "Carlos", "age": 25},
    ]

    schema = inferer.infer(documents)

    assert schema["name"] == "string"
    assert schema["age"] == "integer"


def test_infer_mixed_types():
    inferer = SchemaInferer()

    documents = [
        {"value": 10},
        {"value": 10.5},
    ]

    schema = inferer.infer(documents)

    # float should dominate integer
    assert schema["value"] == "float"


def test_infer_nested_object():
    inferer = SchemaInferer()

    documents = [
        {"user": {"name": "Ana", "active": True}},
        {"user": {"name": "Carlos", "active": False}},
    ]

    schema = inferer.infer(documents)

    assert "user" in schema
    assert isinstance(schema["user"], dict)
    assert schema["user"]["name"] == "string"
    assert schema["user"]["active"] == "boolean"
