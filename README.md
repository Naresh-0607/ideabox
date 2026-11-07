# IdeaBox

IdeaBox is a small, focused idea-management PWA. It provides JWT-authenticated
idea capture, status organization, title search, tag filtering, and responsive
desktop/mobile views.

## Stack

- FastAPI, SQLAlchemy 2, PostgreSQL/Neon, Psycopg 3, Alembic
- Argon2 via `pwdlib` and JWT access tokens
- SvelteKit, TypeScript, and responsive CSS

## Structure

- `backend/`: FastAPI API, SQLAlchemy models, Alembic migrations, and tests
- `frontend/`: SvelteKit client, responsive UI, and PWA assets

## Local Setup

### 1. Backend

1. Navigate to `backend`:
   ```powershell
   cd backend
   ```
2. Copy `.env.example` to `.env` and set `DATABASE_URL` and `JWT_SECRET`.
3. Create and activate a Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
4. Run migrations and start API:
   ```powershell
   alembic upgrade head
   uvicorn main:app --reload
   ```

API documentation will be available at `http://localhost:8000/docs`.

### 2. Frontend

1. Navigate to `frontend`:
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

Access the web app at `http://localhost:5173`.

## Tests

Run backend tests from the `backend` directory:
```powershell
cd backend
pytest
```
