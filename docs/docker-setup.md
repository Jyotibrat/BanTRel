# BanTRel — Local Docker Setup Guide

This guide explains how to run the complete BanTRel stack locally:

- **Backend** — the FastAPI simulation API, packaged with Docker (`Docker` branch of [`Jyotibrat/BanTRel`](https://github.com/Jyotibrat/BanTRel)).
- **Frontend** — the React + Vite dashboard (`UI` branch of the **same** repository), run with the Vite dev server.

The backend talks to SUMO (traffic micro-simulator) and runs a PPO reinforcement-learning agent; the frontend is a dashboard where you configure a simulation and watch PPO compete against a fixed-cycle traffic light.

---

## Architecture at a Glance

```
┌──────────────────────┐        HTTP (JSON)         ┌─────────────────────────────┐
│  Browser             │  ───────────────────────▶  │  FastAPI backend (Docker)   │
│  http://localhost:5173 │   fetch → /simulate etc.  │  http://localhost:7860      │
└──────────────────────┘                            │  ┌───────────────────────┐  │
        ▲                                           │  │ SUMO + netconvert     │  │
        │                                           │  │ PPO checkpoint (.pt)  │  │
        └──── React + Vite dev server (Node) ───────┴──┴───────────────────────┴──┘
```

- The backend runs **entirely inside Docker** — SUMO, Python dependencies and the model download are all handled by the container. Nothing is installed on your machine except Docker.
- The frontend runs **outside Docker** on Node.js (Vite dev server) and calls the backend over HTTP.
- The PPO checkpoint is a small file (~23 KB) downloaded from the Hugging Face Hub (`BJyotibrat/BanTRel-v1.0.0`, public repo) on **first startup only** and cached in a Docker volume, so later restarts are instant.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Windows / macOS / Linux. On Windows, WSL2 backend recommended. The daemon must be **running** before you start. |
| [Node.js](https://nodejs.org/) **20.19+ or 22.12+** | Only needed for the frontend. Required by Vite 8 (`vite ^8.3.0` in the UI branch). `npm` comes with it. |
| Internet access on first run | To pull base images, Python packages and the model checkpoint. |
| ~7 GB free disk | Docker image (SUMO + PyTorch) plus the model cache. |

> **Build time:** the first build is slow — expect roughly 10–25 minutes on a typical laptop. `requirements.txt` pins `torch>=2.2.0`, so pip installs the default PyPI Linux wheel, which pulls in the CUDA runtime (`nvidia-*` packages, several GB). See [Optional: smaller CPU-only image](#optional-smaller-cpu-only-image) if you want to cut this down.

---

## Folder Layout

The backend and frontend are **two branches of the same repository**, so you clone it twice:

```bash
# backend — Docker branch
git clone -b Docker https://github.com/Jyotibrat/BanTRel.git bantrel-backend

# frontend — UI branch of the SAME repo
git clone -b UI https://github.com/Jyotibrat/BanTRel.git bantrel-frontend
```

```
BanTRel Website/          ← your local workspace (not itself a repository)
├── bantrel-backend/      ← Docker branch (this repo)
│   ├── app.py            ← FastAPI application
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example      ← copy to .env
│   └── docs/             ← this documentation
└── bantrel-frontend/     ← UI branch
    ├── .env.example      ← copy to .env
    ├── vite.config.ts    ← dev-server proxy config
    └── src/api/bantrel.ts ← all API calls to the backend
```

Folder names are suggestions — anything works, as long as you run each command in the right one.

---

## Step 1 — Start the Backend (Docker)

Open a terminal in the **backend** folder (`bantrel-backend`).

### 1.1 Configure the environment (optional but recommended)

```bash
cp .env.example .env
```

> The shipped `.env.example` begins with a stray `[TEMPLATE]` marker line. Delete it — Compose tolerates it, but it is confusing in a file you are meant to edit.

For local development the defaults work out of the box:

| Variable | Default | When to change it |
|---|---|---|
| `HF_TOKEN` | *(empty)* | Not needed — the model repo is public. Set it only if you fork the checkpoint into a **private** Hugging Face repo. |
| `BANTREL_CORS_ORIGINS` | `*` | Allow-all is fine for local dev. To restrict, set the frontend origin, e.g. `http://localhost:5173`. |
| `HOST_PORT` | `7860` | Change if port 7860 is already used on your machine. The container always uses 7860 internally. |

> `.env` is git-ignored — never commit it.
>
> **Note on `BANTREL_CHECKPOINT`:** `.env.example` lists it, and `app.py` reads it, but `docker-compose.yml` does not forward it into the container, so setting it in `.env` currently has **no effect**. To make it work, add `- BANTREL_CHECKPOINT=${BANTREL_CHECKPOINT:-}` to the service's `environment:` block and recreate the container. The equivalent download-side override, `BANTREL_CHECKPOINT_FILE`, is not documented in `.env.example` at all.

### 1.2 Build and start

```bash
docker compose up --build
```

**The first run is the slow one** (see Prerequisites). Docker will:

1. Build the image — install SUMO and the Python dependencies, then pre-build the SUMO intersection network (`sumo_config/intersection.net.xml` + `phases.json`). If that network build fails, **the image build fails** — you will see the error in the build output, not in a running container.
2. Start the container — download the PPO checkpoint into the `model_cache` volume.

**Subsequent runs are fast** — the image and checkpoint are cached:

```bash
docker compose up        # foreground, or:
docker compose up -d     # detached (background)
```

### 1.3 Verify the backend is ready

```bash
curl http://localhost:7860/health
```

Expected response:

```json
{
  "status": "ok",
  "network_built": true,
  "checkpoint_found": true,
  "server_time_utc": "2026-10-26 12:00:00 UTC"
}
```

Both `network_built` and `checkpoint_found` must be `true`. If not, see [Troubleshooting](#troubleshooting).

You can also open the interactive API docs at **http://localhost:7860/docs** (Swagger UI), or **http://localhost:7860/redoc**.

---

## Step 2 — Start the Frontend (Vite)

Open a **second** terminal in the **frontend** folder (`bantrel-frontend`).

### 2.1 Configure the API URL

```bash
cp .env.example .env
```

The shipped `.env` already points at the local Docker backend, which is what you want:

```ini
VITE_API_BASE_URL=http://localhost:7860
```

> This must match the port the backend is published on. If you changed `HOST_PORT` in the backend `.env`, change it here too. Trailing slashes are stripped by the app, so either form works.

### 2.2 Install dependencies (first time only)

```bash
npm install
```

### 2.3 Start the dev server

```bash
npm run dev
```

Open **http://localhost:5173** in your browser.

#### Alternative: use the Vite proxy instead of a direct URL

The dev server can proxy API calls, so the browser only ever talks to `localhost:5173` and **CORS never comes into play**:

1. **Remove/comment out** `VITE_API_BASE_URL` in the frontend `.env` (an empty value is what triggers the fallback — leaving it set wins over the proxy).
2. Set the backend target instead:

   ```ini
   BACKEND_URL=http://localhost:7860
   ```

With that, API calls go to `/api/...` on the frontend origin, and `vite.config.ts` forwards them to `BACKEND_URL` while stripping the `/api` prefix. `BACKEND_URL` also defaults to `http://localhost:7860`, so entirely empty config works for the common case.

---

## Step 3 — Verify End-to-End

1. With both terminals running, open **http://localhost:5173**.
2. Go to the **Simulate** page, pick a preset (start with **morning rush**, not the full day — see the note below) and submit.
3. The app submits `POST /simulate`, receives a `job_id`, and **navigates to `/simulate/<job_id>`**, where the Results view polls `GET /simulate/{job_id}` until done and renders charts comparing PPO against fixed-cycle.

Statuses flow `queued → running → done` (or `error`).

> **Runtime:** only one simulation runs at a time server-side. A single preset period finishes in a couple of minutes on a typical laptop; the **full 24-hour day** (`period` omitted, `policy: "both"`) is 8,640 simulation steps × per-vehicle queries × two policies and can take tens of minutes. Start small.

---

## CORS Reference

The browser enforces CORS when the frontend (origin `http://localhost:5173`) calls the backend (`http://localhost:7860`) directly.

- The backend's default `BANTREL_CORS_ORIGINS=*` allows everything — zero config for local dev. This works because the dashboard's `fetch` calls do not send credentials.
- The API is configured with `allow_credentials=True`, so if you ever add credentialed requests (`credentials: 'include'`, cookies), a wildcard origin is rejected by the browser. List the exact origin instead:

  ```ini
  BANTREL_CORS_ORIGINS=http://localhost:5173
  ```

- `.env` changes are **not** picked up by a running container. `docker compose restart` keeps the old environment; recreate the container:

  ```bash
  docker compose up -d
  ```

Symptom of a CORS problem: the UI loads but requests fail, and the browser console shows a "blocked by CORS policy" error.

---

## API Quick Reference

Base URL: `http://localhost:7860`

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Service banner (name, version, docs links) |
| `GET` | `/health` | Liveness/readiness — server, SUMO network, checkpoint |
| `POST` | `/simulate` | Start a simulation job → `{ "job_id": "..." }` |
| `GET` | `/simulate/{job_id}` | Poll status (`queued` / `running` / `done` / `error`) and fetch results |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

`POST /simulate` body:

| Field | Values | Notes |
|---|---|---|
| `mode` | `"preset"` or `"custom"` | required |
| `policy` | `"ppo"`, `"fixed_cycle"`, `"both"` | default `"both"` |
| `period` | `night`, `morning_rush`, `mid_morning`, `afternoon`, `evening_rush`, `evening` | preset mode only |
| `total_vehicles` | integer | custom mode; capped at 60,000 |
| `car_pct` / `motorcycle_pct` / `autorickshaw_pct` | numbers | custom mode; must sum to 100 |
| `n_runs` | 1–3 | default 1; episodes per policy, averaged |
| `deterministic` | boolean | default `true` — argmax instead of sampling the policy |
| `seed` | integer | seeds policy sampling only (see note below) |

Example — start a preset simulation:

```bash
curl -X POST http://localhost:7860/simulate \
  -H "Content-Type: application/json" \
  -d '{"mode": "preset", "policy": "both", "period": "morning_rush"}'
```

Then poll with the returned `job_id`:

```bash
curl http://localhost:7860/simulate/<job_id>
```

Custom demand: use `"mode": "custom"` with `total_vehicles` and a `car_pct` / `motorcycle_pct` / `autorickshaw_pct` mix that sums to 100.

Notes:

- A `period` run is re-anchored to start at `t=0` and simulated in isolation, which is why it is much faster than the full day.
- `deterministic` and `seed` govern **policy action selection only**. The SUMO process is launched with `--random`, so vehicle departures and timings still vary between identical requests — metric values will differ slightly run to run.

---

## Day-to-Day Commands

Run inside the **backend** folder:

```bash
docker compose up -d          # start in background
docker compose logs -f        # follow logs (Ctrl+C to stop following)
docker compose ps             # show container status / health
docker compose down           # stop (model cache volume is kept)
docker compose up --build     # rebuild after backend code changes
docker compose down -v        # stop AND delete the model cache (forces re-download)
```

Daily workflow:

| You changed… | What to do |
|---|---|
| Backend code (`app.py`, `simulation/`, `Dockerfile`, `requirements.txt`) | `docker compose up --build` |
| Backend `.env` | `docker compose up -d` (recreates the container; `restart` will **not** re-read `.env`) |
| Frontend code or frontend `.env` | Nothing — Vite hot-reloads. Restart `npm run dev` if the change doesn't apply. |

---

## Optional: smaller CPU-only image

The simulation runs entirely on CPU, so the CUDA runtime bundled with the default PyPI `torch` wheel is dead weight. To cut the image size substantially and speed up the first build, install CPU-only wheels — e.g. add `--index-url https://download.pytorch.org/whl/cpu` to the `pip install` line in the `Dockerfile`. This is a build-time optimisation only; no application code changes.

---

## Troubleshooting

**`docker compose` fails / can't connect to the Docker daemon**
Docker Desktop isn't running. Start it and wait until it reports "running", then retry.

**Port 7860 already in use**
Set `HOST_PORT=7861` (or any free port) in the backend `.env`, then `docker compose up -d`. Update `VITE_API_BASE_URL` in the frontend `.env` to `http://localhost:7861`.

**The image build fails while installing `sumo` or building the network**
The build runs `netconvert` once (via `simulation/build_network.py`) and fails the whole build if it cannot produce a valid network. Scroll up in the build output for the `netconvert` error — typically an apt/dependency issue. Fix and run `docker compose up --build` again.

**`/health` shows `checkpoint_found: false`**
The checkpoint download failed at container start. Check `docker compose logs -f`. Since the model repo is public, this is almost always a network/proxy problem. After fixing the cause, **recreate** the container so the startup download retries with the new environment:

```bash
docker compose up -d
```

(`docker compose restart` reuses the existing container environment and will not pick up `.env` changes.) The checkpoint lives in the `model_cache` volume, so a successful download persists across restarts; `docker compose down -v` forces a re-download.

**`/health` shows `network_built: false`**
This should not happen after a successful build — the network is compiled during `docker build`, and the API also rebuilds it at startup if the file is missing. If it does, something overwrote `sumo_config/` at runtime (for example a volume mounted over that directory). Rebuild: `docker compose up --build`.

**Job ends with `error` mentioning TraCI / connection / protocol problems**
The container installs SUMO **1.15.0** from the Debian base image, while `requirements.txt` pins `traci==1.20.0` / `sumolib==1.20.0`. If the Python bindings and the `sumo` binary are too far apart, TraCI calls can fail. Align them: pin the Python packages to `1.15.0`, or move to a newer base image that ships a matching SUMO. The job's `trace` field (from `GET /simulate/{job_id}`) shows the exact error.

**Browser console shows CORS errors**
The frontend origin isn't allowed by the backend. For local dev the default `BANTREL_CORS_ORIGINS=*` should prevent this — if you restricted it, add `http://localhost:5173` and recreate the container with `docker compose up -d`. Alternatively switch the frontend to proxy mode (see Step 2.3).

**Simulation results say `error`**
Look at the job's `error`/`trace` fields (via `GET /simulate/{job_id}` or the Results view) and at `docker compose logs -f`. Most cases are invalid request parameters (e.g. vehicle mix not summing to 100, `n_runs` outside 1–3, `total_vehicles` above 60,000).

**Server returns 429 "Server is busy"**
Only one simulation runs at a time, and at most **4 jobs total may be outstanding** (queued plus running). Wait for jobs to finish, or restart the container to clear the in-memory queue (`docker compose restart`). The job store is in-memory — every restart clears it, and completed jobs are purged after 30 minutes.

**Frontend loads but requests fail with nothing in the backend logs**
The frontend is probably pointing at the wrong URL. Confirm `VITE_API_BASE_URL` in the frontend `.env` matches the port the backend is actually published on (`docker compose ps`), then restart `npm run dev`.

**Security note: `.env` is baked into the image**
There is currently no `.dockerignore`, so `COPY . .` in the `Dockerfile` includes `.env`, `.git/` and any local clutter in the build context — meaning a token in `.env` would end up inside an image layer. Add a `.dockerignore` (excluding at least `.env`, `.git/`, `__pycache__/`, `model_files/`, `sumo_config/*.net.xml`, `sumo_config/phases.json`) before building images you intend to share or push.

**Want a completely fresh start**

```bash
docker compose down -v       # also removes the model cache volume
docker compose up --build    # full rebuild + checkpoint re-download
```
