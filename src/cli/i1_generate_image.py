import argparse
import sys
from pathlib import Path

# Add src to path for imports
src_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(src_dir.parent))

from manager.i1_generate_spaces import PromptGenerator
from utils._load_json import load_json
from utils.versioned_storage import load_data, save_data
from utils.enclosed_spaces.random_enclosed_spaces import add_used, subtract


def load_all_scenes() -> dict:
    """Load the enclosed_spaces.json catalog."""
    scenes_path = Path(__file__).resolve().parent.parent / "utils" / "enclosed_spaces" / "enclosed_spaces.json"
    return load_json(str(scenes_path), "")


def generate_and_save(theme: str, n: int = 10, version: int = None) -> dict:
    """
    Generate enclosed spaces for theme and save with versioning.
    - If no file exists: creates v1 with iscomplete=False
    - If file exists and iscomplete=False: loads it (already has data)
    - If file exists and iscomplete=True: creates v2 with new data
    """
    # Load all scenes for the generator
    all_scenes = load_all_scenes()

    # Load existing data
    all_data = load_data(theme)
    version_data = {}
    if version in all_data:
        version_data = all_data.get(version, {})
    
    # Create generator with loaded all_scenes
    generator = PromptGenerator(theme=theme, all_scenes=all_scenes)

    # Generate new enclosed spaces
    new_spaces = generator.generate_enclosed_spaces(n=n, version_data=version_data if version_data else None)
    data_to_save = all_data.copy()
    
    data_to_save[version] = {
        "enclosed_spaces": new_spaces,
        "iscomplete": False,
        "step": 1
    }
    # Save with appropriate version
    save_data(theme, data_to_save)


    return new_spaces


def main():
    parser = argparse.ArgumentParser(description="Generate image prompts for a theme")
    parser.add_argument("theme", help="Theme for the image generation (e.g., residential, gastronomy)")
    parser.add_argument("--n", type=int, default=54, help="Number of enclosed spaces to generate")
    parser.add_argument("--version", type=int, default=1, help="Version identifier for the output (default: v1)")

    args = parser.parse_args()

    generate_and_save(args.theme, args.n, args.version)


if __name__ == "__main__":
    main()
