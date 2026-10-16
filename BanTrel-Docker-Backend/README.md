# BanTRel — Docker Backend

Pure **FastAPI** REST API backend for BanTRel, designed for **local / self-hosted** Docker deployments.

> **HF ZeroGPU version** lives on the `Server` branch of the main repo. This folder is the Docker equivalent — same simulation engine, no Gradio dependency.

---

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows / Mac / Linux)
- Internet access on first run (downloads the PPO checkpoint from Hugging Face Hub)

---

## Quick Start

```bash
# 1. Enter the folder
cd BanTrel-Docker-Backend

# 2. (Optional) configure environment variables
cp .env.example .env
# Edit .env if needed (e.g. set HF_TOKEN for private repos, change HOST_PORT)

# 3. Build the image and start the API
docker compose up --build
```

The API will be available at **http://localhost:7860** after startup.

> **First run takes 2–5 minutes** — Docker builds the image (installs SUMO + Python deps) and downloads the PPO checkpoint (~10 MB). Subsequent starts are instant.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness probe — check if server + network + checkpoint are ready |
| `POST` | `/simulate` | Start a simulation job, returns `{ "job_id": "..." }` |
| `GET` | `/simulate/{job_id}` | Poll job status / retrieve result |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

---

## Testing the API

### 1. Check the server is ready

```bash
curl http://localhost:7860/health
```

Expected:
```json
{
  "status": "ok",
  "network_built": true,
  "checkpoint_found": true,
  "server_time_utc": "2026-10-17 00:00:00 UTC"
}
```

---

### 2. Run a preset simulation (full Bangalore day, PPO vs fixed-cycle)

```bash
curl -X POST http://localhost:7860/simulate \
  -H "Content-Type: application/json" \
  -d '{"mode": "preset", "policy": "both"}'
```

Returns:
```json
{ "job_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }
```

---

### 3. Poll for results

```bash
curl http://localhost:7860/simulate/<job_id>
```

Status flow: `queued` → `running` → `done` (or `error`)

When `done`, the response includes `result.ppo`, `result.fixed_cycle`, and `result.comparison`.

---

### 4. Run a specific time period only

```bash
curl -X POST http://localhost:7860/simulate \
  -H "Content-Type: application/json" \
  -d '{"mode": "preset", "policy": "both", "period": "morning_rush"}'
```

Available periods: `night`, `morning_rush`, `mid_morning`, `afternoon`, `evening_rush`, `evening`

---

### 5. Custom vehicle volume and mix

```bash
curl -X POST http://localhost:7860/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "custom",
    "policy": "both",
    "total_vehicles": 5000,
    "car_pct": 50,
    "motorcycle_pct": 35,
    "autorickshaw_pct": 15
  }'
```

---

### 6. Use the Swagger UI

Open **http://localhost:7860/docs** in your browser — you can trigger all endpoints interactively.

---

## Frontend Integration

Point your frontend's API base URL to `http://localhost:7860`.

For frontend dev servers running on a different port (e.g. `http://localhost:3000`), set in your `.env`:

```
BANTREL_CORS_ORIGINS=http://localhost:3000
```

Then restart: `docker compose down && docker compose up`

---

## Useful Commands

```bash
# Start (background)
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down

# Rebuild after code changes
docker compose up --build

# Check running containers
docker compose ps
```

---

## Architecture

```
BanTrel-Docker-Backend/
├── app.py                  ← FastAPI app (no Gradio, no spaces)
├── download_checkpoint.py  ← Downloads PPO weights from HF Hub
├── simulation/
│   ├── __init__.py
│   ├── baseline.py         ← Fixed-cycle traffic controller
│   ├── build_network.py    ← Builds SUMO intersection network (runs once at build time)
│   ├── demand.py           ← Route/demand file generation
│   ├── env.py              ← SUMO/TraCI gym-style environment
│   ├── model.py            ← PPO ActorCritic neural network
│   └── runner.py           ← Orchestrates simulation jobs
├── sumo_config/            ← SUMO network files (auto-generated at build time)
├── model_files/            ← PPO checkpoint (auto-downloaded at first startup)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```
