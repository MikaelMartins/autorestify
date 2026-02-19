# AutoRESTify

**The High-Performance Runtime Engine for Persistent REST APIs.**

AutoRESTify is an execution engine that transforms JSON collections into complete, persistent, and secure REST APIs. Unlike static code generators, AutoRESTify manages the data lifecycle in real time.

---

## 🚀 Features

- Dynamic route generation
- Automatic schema inference
- SQLite persistence (production-ready)
- Proper in-memory test isolation
- Pluggable security architecture
- Full CRUD support
- Conexão SQLAlchemy (PostgreSQL, MySQL, SQLite, ...)
- CI with GitHub Actions

---

## 📦 Installation

Install from PyPI:

```bash
pip install autorestify
```

With uvicorn server:

```bash
pip install autorestify[server]
```

Or install locally for development:

```bash
git clone https://github.com/MikaelMartins/autorestify.git
cd autorestify
pip install -e .
pip install uvicorn
```

---

## ⚡ Quick Example

```py
from fastapi import FastAPI
from autorestify.api.router_factory import create_router

app = FastAPI()

app.include_router(create_router())
```

Start the server:

```bash
uvicorn main:app --reload
```

---

## 📤 Uploading a collection

Send a JSON payload to the upload endpoint to register a new collection and its documents.

```http
POST /upload
Content-Type: application/json

{
  "collection": "clientes",
  "documents": [
    {"name": "Ana", "age": 30},
    {"name": "Carlos", "age": 25}
  ]
}
```

Once uploaded, the following routes are created automatically for the `clientes` collection:

```
GET    /clientes
GET    /clientes/{id}
POST   /clientes
PUT    /clientes/{id}
DELETE /clientes/{id}
```

---

## 🧠 Architecture Overview

Autorestify is built with:

- FastAPI
- SQLAlchemy
- Modular router factory
- Dynamic schema engine
- Pluggable security layer

Core modules:

```
autorestify/
  api/
  core/
  storage/
  schema/
  security/
```

---

## 🧪 Running Tests

Run the test suite:

```bash
pytest -v
```

Run with coverage reporting:

```bash
pytest --cov=autorestify --cov-report=term-missing
```

---

## 🔐 Security

Security is pluggable. Implement a custom authentication provider by extending the security interface and inject it into the router factory.

---

## 🛠 Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

---

## 🗺 Roadmap

- Filtering support
- Pagination
- Ordering
- Async storage engine
- RBAC
- Multi-tenant architecture

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Mikael Aurio Martins — Software Developer
