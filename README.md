# Codeground Backend
[한국어 README](README.ko.md)


This repository contains a FastAPI based backend service. It provides authentication APIs and uses PostgreSQL through SQLAlchemy and Alembic for migrations.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management
- PostgreSQL instance

## Installation

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd Codeground-Backend
   ```

2. **Install dependencies**

   Use Poetry to install the project requirements:

   ```bash
   poetry install
   ```

3. **Configure environment variables**

   The application loads variables from a `.env` file located **one directory above** the project root. Create `../.env` relative to the repository with values similar to the following:

   ```env
   SECRET_KEY=your-secret-key
   SECRET_KEY_AUTH=your-auth-key
   DB_HOST=localhost
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=codeground
   ```

   These variables are used to construct the database URL for PostgreSQL.

4. **Database setup**

   Initialize the database using Alembic. If no migration files exist, create one:

   ```bash
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```

## Running the Service

Start the FastAPI application with Uvicorn:

```bash
poetry run uvicorn src.app.main:app --reload
```

The API will be available at `http://localhost:8000/`. Authentication endpoints are prefixed with `/api/v1` (e.g. `/api/v1/auth/sign-up`).

## Screen Sharing

The backend includes a minimal WebRTC signalling server exposed via WebSockets. To
start a session, open a connection to `/api/v1/ws/screen-share/{room_id}` where
`{room_id}` is an arbitrary identifier for your room.

1. Any client connecting with the same room ID will receive all messages sent by
   others in that room.
2. The server simply relays text payloads. Typically you send JSON strings that
   contain your WebRTC `offer`, `answer` or `candidate` information.
3. Rooms exist only while clients are connected; once everyone disconnects the
   server forgets the room.

This endpoint is intended as a basic example and does not manage TURN/STUN
servers or advanced signalling logic.
