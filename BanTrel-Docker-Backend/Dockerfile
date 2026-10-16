# BanTRel Docker Backend
# ─────────────────────────────────────────────────────────────────────────────
# Base: Python 3.11 slim (same as HF Spaces default).
# System deps: sumo + sumo-tools (installs netconvert + sumo binary).
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Install SUMO (netconvert + sumo binary via apt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sumo \
    sumo-tools \
    && rm -rf /var/lib/apt/lists/*

ENV SUMO_HOME=/usr/share/sumo
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

WORKDIR /app

# ── Install Python deps first (cached layer) ──────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy source ────────────────────────────────────────────────────────────────
COPY . .

# ── Build the SUMO intersection network once at image build time ───────────────
# This writes sumo_config/intersection.net.xml + sumo_config/phases.json.
# Baking them into the image means no netconvert call per request.
RUN python simulation/build_network.py

# ── Expose API port ────────────────────────────────────────────────────────────
EXPOSE 7860

# ── Start FastAPI via Uvicorn ──────────────────────────────────────────────────
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "7860"]
