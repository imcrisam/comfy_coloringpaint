from pathlib import Path
import json
import os
from typing import Dict, Any


def load_workflow(name: str, base_dir: str) -> Dict[str, Any]:
    """
    Carga un workflow JSON desde base_dir o un path absoluto.
    """
    if os.path.exists(name):
        path = name
    else:
        src_path = Path(__file__).resolve().parents[0] / base_dir
        candidate = src_path / name
        candidate_json = candidate if name.endswith(".json") else candidate.with_suffix(".json")
        if candidate_json.exists():
            path = candidate_json
        else:
            raise FileNotFoundError(f"Workflow JSON no encontrado: {name}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)