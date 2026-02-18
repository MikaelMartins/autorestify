"""
Router Factory for Model2API.

Uses generic collection-based routes instead of
dynamically creating routes at runtime.
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Body, Request

from model2api.core.schema_inference import SchemaInferer
from model2api.core.security import SecurityManager
from model2api.storage.base import Database
from model2api.storage.repository import Repository


def create_router(
    security: SecurityManager | None = None,
    database: Database | None = None,
) -> APIRouter:

    router = APIRouter()

    database = database or Database()
    repository = Repository(database)
    inferer = SchemaInferer()
    security_manager = security or SecurityManager()

    # ----------------------------------
    # Health
    # ----------------------------------

    @router.get("/")
    async def health():
        return {"status": "Model2API running"}

    # ----------------------------------
    # Upload (register collection)
    # ----------------------------------

    @router.post("/upload")
    async def upload(
        request: Request,
        payload: Dict[str, Any] = Body(...),
    ):
        try:
            user = await security_manager.authenticate(request)
            security_manager.authorize_write(user, "system")
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

        collection = payload.get("collection")
        documents = payload.get("documents")

        if not collection:
            raise HTTPException(status_code=400, detail="Missing 'collection'")

        if not isinstance(documents, list):
            raise HTTPException(status_code=400, detail="'documents' must be a list")

        schema = inferer.infer(documents)

        repository.create_tables_from_schema(collection, schema)

        for doc in documents:
            repository.insert(collection, doc)

        return {
            "message": "Collection registered",
            "collection": collection,
            "schema": schema,
        }

    # ----------------------------------
    # Generic CRUD
    # ----------------------------------

    @router.get("/{collection}")
    async def list_items(
        request: Request,
        collection: str,
        limit: int = 100,
    ):
        try:
            user = await security_manager.authenticate(request)
            security_manager.authorize_read(user, collection)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

        if not repository.table_exists(collection):
            raise HTTPException(status_code=404, detail="Collection not found")

        return repository.list(collection, limit)

    @router.get("/{collection}/{item_id}")
    async def get_item(
        request: Request,
        collection: str,
        item_id: int,
    ):
        try:
            user = await security_manager.authenticate(request)
            security_manager.authorize_read(user, collection)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

        item = repository.get(collection, item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return item

    @router.post("/{collection}")
    async def create_item(
        request: Request,
        collection: str,
        payload: Dict[str, Any],
    ):
        try:
            user = await security_manager.authenticate(request)
            security_manager.authorize_write(user, collection)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

        if not repository.table_exists(collection):
            raise HTTPException(status_code=404, detail="Collection not found")

        item_id = repository.insert(collection, payload)

        return {"id": item_id}

    @router.put("/{collection}/{item_id}")
    async def update_item(
        request: Request,
        collection: str,
        item_id: int,
        payload: Dict[str, Any],
    ):
        try:
            user = await security_manager.authenticate(request)
            security_manager.authorize_write(user, collection)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

        ok = repository.update(collection, item_id, payload)

        if not ok:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"status": "updated"}

    @router.delete("/{collection}/{item_id}")
    async def delete_item(
        request: Request,
        collection: str,
        item_id: int,
    ):
        try:
            user = await security_manager.authenticate(request)
            security_manager.authorize_delete(user, collection)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

        ok = repository.delete(collection, item_id)

        if not ok:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"status": "deleted"}

    return router
