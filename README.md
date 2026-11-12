# Exercive

A workout planner for beginner-to-intermediate gym-goers. Pick a training split and the days you
can train, and Exercive builds a weekly schedule, shows how to perform each exercise, and tracks
the sessions you log on a progress calendar.

> **Status:** early development (Phase 0: project setup). The backend and frontend skeletons run
> and talk to each other through a health check. Features arrive phase by phase; see
> [docs/PROGRESS.md](docs/PROGRESS.md).

## Planned features

- Sign up and log in with email and password
- Onboarding questions (goal, experience, equipment, training days) that drive recommendations
- A searchable exercise library with an interactive front/back muscle map
- Step-by-step tutorials per exercise: setup, execution, tempo, breathing, common mistakes
- Preset plans and training splits (Full Body, Upper/Lower, Push/Pull/Legs, and more)
- Workout mode: check off sets, log weight and reps, rest timer
- A monthly progress calendar and a weekly goal tracker with streaks

## Tech stack

| Part     | Tools                                                       |
| -------- | ----------------------------------------------------------- |
| Backend  | Python 3.12, FastAPI, Pydantic, uvicorn                     |
| Frontend | React, TypeScript, Vite, Tailwind CSS                       |
| Tooling  | uv (Python), npm (Node 24), pytest, ruff, Prettier          |
| Later    | SQLAlchemy + Alembic, SQLite locally, PostgreSQL in production |

## Project structure

```
backend/    FastAPI app (app/), tests (tests/), Python dependencies (pyproject.toml, uv.lock)
frontend/   React app (src/), Vite config, Node dependencies (package.json, package-lock.json)
docs/       Progress log and architecture notes
```

In development, two servers run side by side. The browser only talks to the frontend
(port 5173), and the frontend's dev server forwards every request starting with `/api` to the
backend (port 8000).

## Running locally

### 1. Install the tools (once)

You need two tools: **uv**, which installs Python 3.12 and the backend's packages for you, and
**Node.js 24**, which runs the frontend. You don't need to install Python yourself.

**macOS**

- Install [Homebrew](https://brew.sh), the macOS package manager, then uv:
  ```sh
  brew install uv
  ```
- Install Node.js 24 with the macOS installer from [nodejs.org](https://nodejs.org).

**Windows**

- Install uv from PowerShell:
  ```powershell
  winget install --id=astral-sh.uv -e
  ```
- Install Node.js 24 with the Windows installer from [nodejs.org](https://nodejs.org).
- Close and reopen PowerShell so it finds the new `uv` and `node` commands.
- Run every command in this README in **PowerShell**, not Command Prompt (`cmd`). PowerShell
  understands `cp`, and Command Prompt doesn't.

The required Node version is pinned in `.nvmrc`. Check it on either system with
`node --version` (it should start with `v24`) and `uv --version`.

From here on, every command is the same on macOS and Windows.

### 2. Start the backend

```sh
cd backend
cp .env.example .env        # local settings; never commit .env
uv sync                     # installs Python 3.12 and the exact versions in uv.lock
uv run uvicorn app.main:app --reload
```

The API now runs at http://localhost:8000. Check it at
http://localhost:8000/api/health, or browse the interactive API docs at
http://localhost:8000/api/docs.

### 3. Start the frontend

In a second terminal:

```sh
cd frontend
npm ci                      # installs the exact versions in package-lock.json
npm run dev
```

Open http://localhost:5173. The page should show **Connected (development)**. If it shows
**API unreachable**, check that the backend from step 2 is still running.

No `.env` file is needed for the frontend. `frontend/.env.example` lists the one setting you
can override.

## Checks

Run these before opening a pull request.

**Backend** (from `backend/`):

```sh
uv run pytest               # tests
uv run ruff check .         # linter: likely bugs, docstrings, type hints
uv run ruff format .        # formatter (add --check to only report)
```

**Frontend** (from `frontend/`):

```sh
npm run typecheck           # TypeScript type check
npm run format              # Prettier (format:check to only report)
npm run build               # production build into dist/
```

## Licence

[MIT](LICENSE)
