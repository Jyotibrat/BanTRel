"""
Downloads the PPO checkpoint from the HF Hub model repo into model_files/,
so the weights don't need to be committed into the git repo.

Used two ways:
  * imported by app.py at startup via ensure_checkpoint()
  * run directly: python download_checkpoint.py

Requires the HF_TOKEN env var only if the model repo is private.
"""

import os
import shutil

from huggingface_hub import hf_hub_download

REPO_ID = "BJyotibrat/BanTRel-v1.0.0"
FILENAME = (
    os.environ.get("BANTREL_CHECKPOINT_FILE", "").strip()
    or "Model/Phase 2/PyTorch Model/ppo_bangalore.pt"
)

DEFAULT_DEST = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "model_files", "ppo_bangalore.pt"
)


def ensure_checkpoint(dest_path: str = None) -> str:
    """Ensure the PPO checkpoint exists at dest_path and return that path.

    Skips the download if the file already exists (idempotent).
    hf_hub_download caches to the default HF cache, then we copy it to a
    flat, predictable location for easy volume-mounting in Docker.
    """
    dest_path = (dest_path or "").strip() or DEFAULT_DEST
    if os.path.exists(dest_path):
        return dest_path

    print(f"[BanTRel] Downloading checkpoint {REPO_ID}/{FILENAME} …")
    cached_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        token=os.environ.get("HF_TOKEN") or None,
    )
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(cached_path, dest_path)
    print(f"[BanTRel] Checkpoint saved to: {dest_path}")
    return dest_path


if __name__ == "__main__":
    print(f"Checkpoint ready at: {ensure_checkpoint()}")
