"""
Downloads the PPO checkpoint from the HF Hub model repo into model_files/,
so the weights don't need to be committed into the Space's git repo.

Used two ways:
  * imported by app.py, which calls ensure_checkpoint() at startup
  * run by hand:  python download_checkpoint.py

Requires the HF_TOKEN env var only if the model repo is private.
"""

import os
import shutil

from huggingface_hub import hf_hub_download

REPO_ID = "BJyotibrat/BanTRel-v1.0.0"
# Path of the file inside the model repo (note the subfolders and spaces).
FILENAME = os.environ.get(
    "BANTREL_CHECKPOINT_FILE", "Model/Phase 2/PyTorch Model/ppo_bangalore.pt"
)

DEFAULT_DEST = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "model_files", "ppo_bangalore.pt"
)


def ensure_checkpoint(dest_path: str = DEFAULT_DEST) -> str:
    """Make sure the checkpoint exists at dest_path and return that path.

    hf_hub_download keeps the repo's folder structure when local_dir is used,
    so the file is fetched into the normal HF cache and then copied to a flat,
    predictable location.
    """
    if os.path.exists(dest_path):
        return dest_path

    cached_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        token=os.environ.get("HF_TOKEN") or None,
    )
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(cached_path, dest_path)
    return dest_path


if __name__ == "__main__":
    print(f"Checkpoint ready at: {ensure_checkpoint()}")