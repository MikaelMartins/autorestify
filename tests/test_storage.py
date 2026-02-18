import pytest

from model2api.storage.base import Database
from model2api.storage.repository import Repository


def test_crud_operations(tmp_path):
    db_file = tmp_path / "test.db"
    database = Database(database_url=f"sqlite:///{db_file}")
    repository = Repository(database)

    schema = {
        "name": "string",
        "age": "integer",
    }

    repository.create_tables_from_schema("users", schema)

    # INSERT
    user_id = repository.insert("users", {"name": "Ana", "age": 30})
    assert user_id == 1

    # GET
    user = repository.get("users", user_id)
    assert user["name"] == "Ana"
    assert user["age"] == 30

    # UPDATE
    updated = repository.update("users", user_id, {"age": 31})
    assert updated is True

    user = repository.get("users", user_id)
    assert user["age"] == 31

    # LIST
    users = repository.list("users")
    assert len(users) == 1

    # DELETE
    deleted = repository.delete("users", user_id)
    assert deleted is True

    user = repository.get("users", user_id)
    assert user is None
