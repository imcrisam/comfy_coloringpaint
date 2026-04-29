import json
from pathlib import Path


def get_output_dir() -> Path:
    """Get the output directory path."""
    return Path(__file__).resolve().parents[2] / "output"


def load_data(theme: str) -> dict:
    """
    Load existing versioned data for theme.
    Returns: (enclosed_spaces, version, iscomplete)
    """
    output_path = get_output_dir() / f"{theme}.json"

    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return data

    return {}


def save_data(theme: str, data: dict):
    """Save enclosed_spaces with versioning. If file exists, increment version."""
    get_output_dir().mkdir(parents=True, exist_ok=True)

    output_path = get_output_dir() / f"{theme}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
