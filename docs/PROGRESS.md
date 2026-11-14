# Progress

## 2026-11-13 onwards: Phase 1, database (in progress, branch `feat/database`)

### Built
- SQLAlchemy 2.1.8 added to the backend.
- `database_url` setting in `backend/app/config.py`, documented as `DATABASE_URL` in `backend/.env.example`. It defaults to a SQLite file at `backend/exercive.db` (already in `.gitignore`).
- `backend/app/db.py`: the engine, the `SessionLocal` session factory, the `Base` class for models, and `get_db`, the per-request session dependency (written by me).

### Key decisions
- **The SQLite default path is absolute, built from `BACKEND_DIR`:** a relative path like `sqlite:///./exercive.db` depends on the folder you start the server from, so running from the repo root would silently create a second, empty database.
- **`check_same_thread=False` only for SQLite:** FastAPI runs sync routes on a pool of worker threads, and SQLite by default refuses a connection used from a different thread than the one that opened it. PostgreSQL has no such rule, so the option is only passed when the URL starts with `sqlite`.
- **`get_db` creates the session before `try`, and closes it in `finally`:** if creating it failed inside the `try`, `finally` would hit an undefined variable. `finally` is the only place guaranteed to run when the route raises.

### Left to do
- First models (User, Muscle, Equipment, Exercise, ExerciseMuscle), then Alembic migrations, the seed script (check dataset licences first), and the DBeaver walkthrough. Add the Ruff extension for VS Code.

### What I learned
- **Database:** where the app keeps data permanently, so it survives a restart.
- **SQL:** the language databases understand (`SELECT name FROM exercises WHERE muscle = 'chest'`).
- **SQLite vs PostgreSQL:** SQLite is a whole database in one file with nothing to install, good for local dev. PostgreSQL runs as a separate server and handles many users at once, used in production.
- **SQLAlchemy (an ORM):** a Python library that turns Python into SQL. The same code works on SQLite and PostgreSQL, so switching only means changing `DATABASE_URL`.
- **Engine vs session:** the engine is the phone line to the database, set up once. A session is one phone call, opened per request and always hung up afterwards.
- **Thread:** a worker inside a program. Several threads let FastAPI handle several requests at once.
- **`yield` with `try/finally`:** `yield` hands a value out and pauses. If the route crashes, the error comes out at the `yield`, so code after it is skipped; only `finally` is guaranteed to run.

## 2026-10-30 to 2026-11-12: Phase 0, project setup (complete, merged as PR #3)

### Built
- Repo setup: extended `.gitignore`, pinned Node 24 and Python 3.12.
- Backend skeleton: FastAPI app, typed settings from environment variables, `GET /api/health`, `backend/.env.example`.
- Empty `models`, `services` and `seed` packages for later phases.
- Backend tests with pytest, and linting and formatting with ruff.
- First test and lint run: 5 tests passed, ruff clean, on Python 3.12 in a temporary environment.
- Frontend skeleton: Vite, React and strict TypeScript, an `/api` dev proxy to the backend, a typed client for `GET /api/health`, and an `App` that shows the API status.
- Prettier for the frontend: `npm run format` and `npm run format:check`, plus format on save in VS Code (`.vscode/settings.json`). The folder was first committed as `vscode/` (no dot), which VS Code ignores; renamed on 2026-11-06.
- Tailwind CSS v4 through its Vite plugin, with the "old money" colour and font tokens in `frontend/src/styles/index.css`.
- Self-hosted web fonts (Inter and Cormorant Garamond, variable versions) through Fontsource, and the first styled page: the health-check card in `App.tsx` uses the tokens (brass dot when connected, oxblood box on error, `aria-live` so screen readers announce the change).
- Backend tests and ruff now run on the local uv install: 5 tests passed, ruff clean.
- Frontend branch merged to `main` as PR #2 (2026-11-10). The remaining docs work happened on `docs/phase-0`.
- `README.md`: what the project is, planned features, stack, folder layout, local setup for macOS and Windows, and the check commands. The commands were run before being written down; the Windows steps are untested.
- `docs/ARCHITECTURE.md`: system diagram (browser, Vite dev server, FastAPI, planned database), a folder-by-folder map of what is built and what is planned, a step-by-step trace of `GET /api/health`, and the production plan.

### Key decisions
- **uv for Python tooling:** one tool manages the Python version, dependencies and lockfile, and runs 3.12 alongside other Python versions on the same machine.
- **All routes under `/api`:** the plan is for the browser to reach the API on the frontend's own origin, through a proxy. Browsers such as Safari block cross-site cookies, which would break the httpOnly login cookie if the frontend and backend were on different domains. The proxy is not built yet.
- **Ruff enforces docstrings and type hints:** the project rule is checked automatically, not just by review.
- **`httpx2` instead of `httpx` for tests:** Starlette deprecates `httpx` for its test client.
- **`db.py` and Alembic moved to Phase 1:** nothing uses a database yet.
- **Prettier pinned to an exact version (no `^`):** even minor releases can change formatting, so two developers on different 3.x versions would keep reformatting each other's files.
- **Prettier runs on `.` with a `.prettierignore`:** everything is checked by default, and exclusions (the lockfile, `dist/`) live in one place. Listing only `src/` would have skipped the config files.
- **VS Code formats only frontend file types with Prettier:** `prettier.requireConfig` keeps it out of files without a config, such as the root README. The Ruff extension for Python gets added at Phase 1.
- **Tailwind is a devDependency, pinned to exact 4.3.3:** it runs at build time and only its CSS output reaches the browser. 4.3.4 and 4.3.5 were days old when we installed, and a `^` range had already pulled in 4.3.5 once, so upgrades are now a deliberate choice.
- **Colour tokens are named by role, not hue** (`accent`, not `brass`): the optional light theme can swap values without renaming classes. Tailwind's default palette is removed so off-palette colours can't creep in.
- **Oxblood (`danger`) is a background colour only:** as text on the dark background it's about 1.7:1 contrast, below WCAG AA's 4.5:1. Ivory text on oxblood is about 9:1.

- **Fonts are self-hosted with Fontsource, not loaded from Google Fonts:** visitors' browsers never contact Google, the fonts still work offline (needed for the PWA), and the versions are pinned in the lockfile. Variable versions, so one file covers every weight, and the browser only downloads the character-set files the page uses (`unicode-range`).
- **Font tokens use Fontsource's registered names** (`'Inter Variable'`, `'Cormorant Garamond Variable'`). Plain `'Inter'` would silently fall back to the backup font.
- **Fonts are `dependencies`, pinned to exact 5.3.0:** the font files ship to the browser, like React. Pinned because Fontsource's version number describes the npm package, not the typeface: a patch release can refresh the font files, change letter widths and make text wrap differently, with no code change on our side.
- **Diagrams are written in Mermaid inside the Markdown:** GitHub draws them, and they live in the repo as text, so a change to the design shows up as a normal diff. Unbuilt parts are drawn dashed or marked "planned", so the doc never claims more than exists.
- **`docs/ARCHITECTURE.md` is public, like this file:** it is re-included in `.gitignore`. Private learning notes stay out of it.
- **README uses `npm ci`, not `npm install`, for first setup:** `npm ci` installs exactly what the lockfile records and fails if `package.json` and the lockfile disagree, so setup can't silently change the lockfile.
- **Windows setup is documented, a `.gitattributes` file is not (yet):** Git for Windows defaults to CRLF line endings on checkout, which would make `npm run format:check` fail on every file. Only the macOS developer exists today and CI will run on Linux, so it waits until a Windows contributor appears. The fix is one line, `* text=auto eol=lf`, rather than telling Prettier to accept mixed endings.
- **Merge commits, and delete the branch after merging:** the commits are already in `main`, so deleting only removes the label. Optional: turn on "Automatically delete head branches" in the GitHub repo settings.

### Left to do
- ~~Your review of Phase 0, then merge `docs/phase-0`.~~ Done: merged as PR #3.
- **Phase 1** (suggested branch `feat/database`): `db.py`, SQLAlchemy models, Alembic migrations, seed script for the exercise dataset (check licences first), and a DBeaver walkthrough. Add the Ruff extension for VS Code at the same time.
- Deferred on purpose: `.gitattributes` for Windows line endings (see decisions), the production `/api` proxy on the frontend host (Phase 9), and the optional GitHub setting "Automatically delete head branches".

### What I learned
**Project setup**
- **Dependency:** code other people wrote that a project relies on, listed in a file so any machine can install the same set.
- **uv:** installs Python packages and manages Python versions.
- **Virtual environment:** a private folder of packages for one project, so projects can't clash.
- **`pyproject.toml` vs `uv.lock`:** the first lists what the project needs as version ranges. The second records the exact versions installed and is generated, so it gets committed but never edited.

**Environment variables**
- **Environment variables:** values a program gets from where it runs, separate from its code, so the same code can behave differently locally and in production.
- **`.env` vs `.env.example`:** `.env` holds real values and is never committed. `.env.example` is the safe template that is committed.
- **Never commit a secret:** git keeps history, so deleting it later doesn't help. It has to be replaced with a new one.
- **Not everything goes in `.env`:** it holds the app's own secrets. User emails and hashed passwords go in the database.
- **Production has no `.env` file:** the same values are entered in the hosting provider's settings.

**How the backend works**
- **API:** the set of requests a backend agrees to answer. The frontend asks the API and never touches the database directly.
- **Endpoint:** one specific request the API answers, like `GET /api/health`.
- **Status code:** a number showing how a request went. `200` means success and `404` means not found.
- **Router:** a group of related endpoints in one file.
- **Schema:** the agreed shape of the data going in and out.
- **Web server (uvicorn):** listens for requests and passes them to FastAPI.
- **Dependency injection (`Depends`):** FastAPI passes in what a function needs, and tests can swap in something else.

**Tools and git**
- **Tests:** `TestClient` sends simulated requests through the app without starting a server.
- **Linter and formatter:** `ruff check` finds likely mistakes and rule breaks. `ruff format` makes the layout consistent.
- **`.gitignore`:** lists files git should never track.
- **Staging by name:** `git add <file>` stages only that file, while `git add .` stages everything, including files you didn't mean to commit.
- **`.vscode/`:** where VS Code keeps project settings. It can be created by the editor rather than by a command you ran.

**Frontend tooling**
- **`package.json`:** the frontend's manifest: project info, scripts (named command shortcuts) and dependencies. The frontend's version of `pyproject.toml`.
- **`dependencies` vs `devDependencies`:** the test is whether the code runs in the user's browser. React does; Prettier and TypeScript only run on a developer's machine or in CI.
- **`^` vs an exact version:** `^19.3.1` allows any newer 19.x; `3.9.10` allows only that version.
- **Lockfile (`package-lock.json`):** records the exact version and an integrity fingerprint of every installed package, so every machine installs identical code. That's the reason to commit it.
- **Formatter vs linter:** a formatter (Prettier, `ruff format`) changes how code looks. A linter (`ruff check`) reports likely bugs and rule breaks.
- **npm acts on the current folder:** running `npm install` from the repo root created a stray `package.json` there.
- **A range is permission, the lockfile is the record:** `^4.3.3` lets npm pick any newer 4.x, so it installed 4.3.5. `-E` saves an exact version; `-D` puts a package in `devDependencies`.
- **Each project has its own copy of a package** in `node_modules/`, installed from the lockfile. What's installed globally on someone's machine doesn't matter.
- **Utility-first CSS (Tailwind):** small single-purpose classes on the element (`bg-surface p-4`) instead of hand-written CSS rules. Only the classes actually used end up in the CSS file.
- **Exit codes and CI:** 0 means success, anything else means failure, and CI only reads that number. A check that exits 0 without checking anything is a silent false pass, so make every new check fail once on purpose.
- **Pinning:** writing an exact version with no `^` (`"5.3.0"`), so npm can never move it on its own. If you edit `package.json` by hand, run `npm install` afterwards so the lockfile's copy of the range matches.
- **Diff:** the lines that changed since your last commit (`-` removed, `+` added). A brand-new dependency shows only `+` lines, because git never saw an earlier version. Git opens long output in a pager: press `q` to leave, or use `git --no-pager`.
- **Virtual environment label `(exercive-backend)` in the terminal:** the Python environment is active. It comes from `name` in `pyproject.toml`, and VS Code switches it on automatically. `deactivate` turns it off for that terminal.
- **`@font-face` and `unicode-range`:** tell the browser where a font file is and which characters it covers, so it only downloads the files the page needs.
- **Merged branches:** merging doesn't delete a branch on GitHub. Deleting it is safe and normal (`git branch -d` refuses if the work isn't merged).
- **`npm install` vs `npm ci`:** `package.json` is the manifest (allowed version ranges) and the lockfile is the record (chosen versions). `npm install` reconciles the two and may rewrite the lockfile: when they are out of sync, when a package is added, or when npm versions differ. If the lockfile already satisfies `package.json`, it does not upgrade anything. `npm ci` treats the lockfile as the truth: it installs exactly that, errors on a mismatch, and never writes to it.
- **Four parts of a URL:** in `http://localhost:5173/api/health`, the scheme (`http`) is how to talk, the host (`localhost`) is which machine, the port (`5173`) is which program on it, and the path (`/api/health`) is what is being asked for. The Vite proxy decides by the path alone: forward if it starts with `/api`.
- **The dev server answers unknown paths with the app's HTML:** `GET /health` on port 5173 returns status 200 and `index.html`, not a 404, because Vite serves a single-page app. A mistyped API path in the frontend therefore fails when parsing JSON, not with an error status.
- **CI (continuous integration):** a fresh cloud machine that installs from the lockfile and runs your checks on every push and PR. Built in Phase 9.
