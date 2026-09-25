# BanTRel Frontend

A Vite + React + TypeScript frontend for **BanTRel** — a PPO reinforcement learning agent that optimizes traffic signal control at a 4-way Bangalore intersection, benchmarked against a fixed-cycle baseline via SUMO simulations.

## Prerequisites

- Node.js 18+
- The deployed **BanTRel FastAPI backend** on Hugging Face Spaces (or locally)

## Setup

```bash
# 1. Copy the environment file and fill in your HF Space URL
cp .env.example .env
# Edit .env:
# VITE_API_BASE_URL=https://your-username-bantrel.hf.space

# 2. Install dependencies
npm install

# 3. Start the dev server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `VITE_API_BASE_URL` | **Yes** | Base URL of the BanTRel FastAPI backend (no trailing slash). Example: `https://your-hf-space.hf.space` |

Without `VITE_API_BASE_URL` set, the app will render all UI but API calls will fail.

## Project Structure

```
src/
├── api/bantrel.ts           # All API calls (POST /simulate, GET /simulate/:id)
├── types/simulation.ts      # TypeScript interfaces matching the API exactly
├── hooks/
│   ├── useSimulationJob.ts  # Polling hook for job status
│   └── useDemandForm.ts     # Form state, validation, submit logic
├── components/
│   ├── ui/                  # Shared primitives (Button, Card, Badge, Tooltip)
│   ├── layout/              # NavBar, Footer
│   ├── simulate/            # Form sub-components
│   └── results/             # Results sub-components (charts, table, states)
└── pages/
    ├── Landing.tsx
    ├── Simulate.tsx
    ├── Results.tsx
    ├── About.tsx
    └── NotFound.tsx
```

## Routes

| Route | Page |
|---|---|
| `/` | Landing — hero, stats, intersection schematic |
| `/simulate` | Configure simulation form |
| `/simulate/:jobId` | Results — polls until done/error |
| `/about` | RL setup explanation |
| `*` | 404 Not Found |

## Tech Stack

- **Vite** + **React 18** + **TypeScript**
- **React Router v6** — client-side routing
- **Tailwind CSS v4** — design tokens from Stitch design system
- **Recharts** — time-series metric charts
- **Google Fonts**: Space Grotesk (headlines), Inter (body), JetBrains Mono (telemetry)

## Design System

Colors, typography, and spacing are extracted from the **Stitch project** `16035188452262981512` ("BanTRel Traffic Simulation Dashboard"). All design tokens are defined in `src/index.css` via Tailwind v4 `@theme`.

## Build

```bash
npm run build   # Production build to dist/
npm run preview # Preview production build
```

## API Contract

See [`src/api/bantrel.ts`](src/api/bantrel.ts) and [`src/types/simulation.ts`](src/types/simulation.ts) for the full typed contract.

Key endpoints:
- `POST /simulate` — submit job, returns `{ job_id }`
- `GET /simulate/{job_id}` — poll status: `queued | running | done | error`
