import random

from prompts.flux_coloring_paint import build_prompt
from utils.enclosed_spaces.random_enclosed_spaces import pick_random, subtract

class PromptGenerator:

    def __init__(self, theme: str, all_scenes: dict):
        self.all_scenes = all_scenes
        self.theme = theme

    def _flatten(self, catalog: dict) -> list[tuple]:
        """Convert catalog dict into a flat list of (location, sub_location) tuples."""
        pairs = []
        for locations in catalog.values():
            for location, sub_locations in locations.items():
                for sub in sub_locations:
                    pairs.append((location, sub))
        return pairs

    def generate_enclosed_spaces(self, n: int, version_data: dict = None) -> list[str]:
        remaining = subtract(self.all_scenes, version_data.get("enclosed_spaces", {})) if version_data else self.all_scenes

        picked = pick_random(remaining, n)
        return picked