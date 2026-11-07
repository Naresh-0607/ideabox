# IdeaBox

IdeaBox is a small, focused idea-management PWA. It provides JWT-authenticated
idea capture, status organization, title search, tag filtering, and responsive
desktop/mobile views.

## Stack

- FastAPI, SQLAlchemy 2, PostgreSQL/Neon, Psycopg 3, Alembic
- Argon2 via `pwdlib` and JWT access tokens
- SvelteKit, TypeScript, and responsive CSS

## Structure

- `main.py`, `routers.py`, `schemas.py`, `security.py`: API and auth
- `models.py`, `database.py`: SQLAlchemy models and sessions
- `migrations/`: Alembic migrations
- `frontend/`: SvelteKit client and PWA assets

## Local setup

1. Copy `.env.example` to `.env` and set `DATABASE_URL` and a long `JWT_SECRET`.
2. Create and activate a Python environment, then install dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Apply migrations and start the API:

   ```powershell
   alembic upgrade head
   uvicorn main:app --reload
   ```

   API documentation is available at `http://localhost:8000/docs`.

4. Start the frontend:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

## Tests

Run backend tests with `pytest`. The API uses the configured database; for an
isolated local run set `DATABASE_URL=sqlite:///./test.db`.

Never commit `.env`, credentials, JWT secrets, or database URLs.
