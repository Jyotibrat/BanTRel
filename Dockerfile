FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    sumo sumo-tools \
    && rm -rf /var/lib/apt/lists/*

ENV SUMO_HOME=/usr/share/sumo
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
ENV PIP_DEFAULT_TIMEOUT=1000
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build the (fixed) network + phase strings once, at image build time,
# not on every request. sumo_config/*.xml and phases.json get baked in.
RUN python simulation/build_network.py

# Place your downloaded checkpoint at model_files/ppo_bangalore.pt before
# building, OR set BANTREL_CHECKPOINT to a path you fetch at container
# startup (e.g. via huggingface_hub.hf_hub_download in an entrypoint script).

EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
