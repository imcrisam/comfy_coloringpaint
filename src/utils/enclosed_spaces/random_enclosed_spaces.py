import json
import random


def pick_random(catalog: dict) -> dict:
    """Pick a random category, location and sub_location from the catalog."""
    category = random.choice(list(catalog.keys()))
    location = random.choice(list(catalog[category].keys()))
    sub_location = random.choice(catalog[category][location])
    return {category: {location: [sub_location]}}


def subtract(catalog: dict, used: dict) -> dict:
    """Return only the entries from catalog that are not in used."""
    remaining = {}
    for category, locations in catalog.items():
        for location, sub_locations in locations.items():
            used_subs = used.get(category, {}).get(location, [])
            leftover = [s for s in sub_locations if s not in used_subs]
            if leftover:
                remaining.setdefault(category, {})[location] = leftover
    return remaining


def add_used(used: dict, new: dict) -> dict:
    """Merge new picked entry into used dict and return the result."""
    for category, locations in new.items():
        for location, sub_locations in locations.items():
            existing = used.setdefault(category, {}).setdefault(location, [])
            for sub in sub_locations:
                if sub not in existing:
                    existing.append(sub)
    return used