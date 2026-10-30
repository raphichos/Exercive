# Progress

## 2026-10-30: Phase 0 (in progress)

### Built
- Repo setup: extended `.gitignore`, pinned Node 24 and Python 3.12.
- Backend skeleton: FastAPI app, typed settings from environment variables, `GET /api/health`, `backend/.env.example`.
- Empty `models`, `services` and `seed` packages for later phases.
- Backend tests with pytest, and linting and formatting with ruff.
- First test and lint run: 5 tests passed, ruff clean, on Python 3.12 in a temporary environment.

### Key decisions
- **uv for Python tooling:** one tool manages the Python version, dependencies and lockfile, and runs 3.12 alongside other Python versions on the same machine.
- **All routes under `/api`:** the plan is for the browser to reach the API on the frontend's own origin, through a proxy. Browsers such as Safari block cross-site cookies, which would break the httpOnly login cookie if the frontend and backend were on different domains. The proxy is not built yet.
- **Ruff enforces docstrings and type hints:** the project rule is checked automatically, not just by review.
- **`httpx2` instead of `httpx` for tests:** Starlette deprecates `httpx` for its test client.
- **`db.py` and Alembic moved to Phase 1:** nothing uses a database yet.

### Left to do
- Run the backend setup and tests on a local uv install (the first run used a temporary one).
- Frontend skeleton: Vite, React, TypeScript, Tailwind theme tokens, prettier, and a page that calls `/api/health` through the proxy.
- README: what the project is and how to run it locally.
- Architecture diagram and notes in `docs/`.
