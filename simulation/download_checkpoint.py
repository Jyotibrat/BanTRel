"""
Downloads the PyTorch checkpoint from your HF Hub model repo into
model_files/, so the Dockerfile doesn't need the weights committed
directly into the Space's git repo (keeps the repo small, and lets you
swap in a new checkpoint by just re-running this).

Usage: python download_checkpoint.py
Requires HF_TOKEN env var only if the model repo is private.
"""

import os

from huggingface_hub import hf_hub_download

REPO_ID = "BJyotibrat/BanTRel-v1.0.0"
# Update this to the exact filename in your HF repo if it differs.
FILENAME = "Model/Phase 2/PyTorch Model/ppo_bangalore.pt"
OUT_DIR = os.path.join(os.path.dirname(__file__), "model_files")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        local_dir=OUT_DIR,
        token=os.environ.get("HF_TOKEN"),
    )
    import shutil
    final_path = os.path.join(OUT_DIR, "ppo_bangalore.pt")
    shutil.move(path, final_path)
    print(f"Downloaded and moved checkpoint to: {final_path}")

