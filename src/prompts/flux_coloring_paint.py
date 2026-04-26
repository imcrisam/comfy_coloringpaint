import json
import random
from pathlib import Path

# ──────────────────────────────────────────────
# OPTIONS
# ──────────────────────────────────────────────

OPTIONS = {
    "structural": {
        "description": "Elements visible and distinguishable in black & white",
        "room_type": [
            "bathroom",
            "kitchen",
            "bedroom",
            "library / reading room",
            "coffee shop corner",
            "gaming room",
            "witch's apothecary",
            "home studio",
            "greenhouse",
            "art studio",
        ],
        "wall_style": [
            "warm paneling with decorative vertical lines",
            "exposed brick texture with climbing ivy",
            "painted planks with rustic knots",
            "delicate floral wallpaper with subtle repeating pattern",
            "smooth plaster with framed botanical prints",
            "stone blocks with hanging lanterns",
            "tiled mosaic with geometric patterns",
            "shiplap boards with vintage signage",
        ],
        "floor_pattern": [
            "checkered tiles with a simple geometric pattern",
            "worn hardwood planks with visible grain",
            "hexagonal mosaic tiles",
            "cobblestone with subtle mortar lines",
            "plush area rug over smooth floorboards",
            "terracotta tiles with hand-painted motifs",
            "polished marble with natural veining",
        ],
        "focal_piece": [
            "a prominent clawfoot bathtub with wooden feet and a plank tray holding a ceramic cup and a candle",
            "a large rustic farmhouse kitchen island cluttered with cooking utensils and fresh herbs",
            "a cozy canopy bed draped with flowing sheer curtains and layered quilts",
            "a floor-to-ceiling antique bookcase overflowing with colorful books and trinkets",
            "a vintage espresso bar cart loaded with coffee equipment and small pastries",
            "a glowing desktop setup with multiple monitors, a mechanical keyboard, and LED accents",
            "a large wooden workbench covered in art supplies, half-finished canvases, and paint tubes",
            "a grand antique fireplace with a carved mantle holding framed photos and candelabras",
            "a large ornate vanity table with a lighted mirror surrounded by perfume bottles and jewelry",
            "a hanging macramé hammock strung between two wooden pillars surrounded by potted plants",
        ],
        "left_furniture": [
            "a multi-level wooden shelf holds stacked towels, cosmetic bottles, and decorative jars, with fluffy slippers below",
            "a tall pantry cabinet with glass doors displaying neatly arranged spice jars and cookbooks",
            "a wooden wardrobe with a partially open door revealing folded clothes and hanging garments",
            "a rolling wooden cart with art supplies, brushes in mason jars, and stacked sketchbooks",
            "a vintage record player cabinet with stacked vinyl records and a small speaker",
            "a pegboard wall organizer filled with hanging tools, plants, and small shelves",
            "a small reading nook with a built-in bench, cushions, and stacked books below",
        ],
        "right_furniture": [
            "a wooden vanity cabinet with small legs, a sink basin, chrome faucet, and a rounded mirror with a flower accent above",
            "an antique writing desk with a banker's lamp, quill pen stand, and ink bottles",
            "a kitchen counter with a wooden cutting board, hanging pots, and a window herb garden above",
            "a nightstand with a stack of books, a glowing lamp, and a small succulent plant",
            "a small bar cabinet with glass doors, decanters, and hanging stemware",
            "a makeup station with a lighted mirror, brush holders, and tiered organizers",
            "a tall cactus in a woven basket next to a floating wooden shelf with small figurines",
        ],
        "decorative_details": [
            "a potted plant with large broad leaves",
            "a frog-shaped bath mat with a small crown",
            "a hanging loofah and a patterned towel",
            "fairy lights draped along the ceiling",
            "a small cat curled up in a cozy corner",
            "stacked vintage suitcases used as side tables",
            "wind chimes hanging near a small window",
            "a wall clock with roman numerals",
            "a collection of crystals and small geodes on a windowsill",
            "a small bird in a decorative cage",
            "candles of various heights on a tray",
            "a small chalkboard with a handwritten message",
        ],
    },
    "visual": {
        "description": "Elements related to color, lighting, and mood — indistinguishable in black & white",
        "art_style": [
            "thick, clean, bold black outlines and a soft pastel color palette",
            "thin ink outlines with a muted earthy color palette",
            "crisp vector outlines with a bright saturated color palette",
            "hand-drawn sketch outlines with a warm sepia color palette",
            "fine line art with a cool monochromatic color palette",
            "chunky pixel-art outlines with a retro 16-bit color palette",
        ],
        "mood": [
            "warm, Lo-Fi Cozy",
            "magical and whimsical",
            "calm and zen",
            "moody and atmospheric",
            "festive and cheerful",
            "mysterious and enchanted",
            "minimalist and airy",
            "romantic and soft",
        ],
        "lighting": [
            "soft diffused natural light from a small window",
            "warm golden lamplight casting a gentle glow",
            "cool moonlight filtering through sheer curtains",
            "ambient candlelight with soft flickering shadows",
            "bright overhead light with clean even illumination",
            "dappled afternoon sunlight through a skylight",
        ],
    },
}


# ──────────────────────────────────────────────
# PROMPT BUILDER
# ──────────────────────────────────────────────

PROMPT_TEMPLATE = (
    "A highly detailed, cozy isometric illustration of a stylized miniature {room_type}, "
    "enclosed within a decorative rounded room frame. "
    "The art style is defined by {art_style}. "
    "The perspective is a consistent, high isometric view. "
    "All shapes are simple, charming, and detailed with minimal complex shading. "
    "The entire scene has a {mood} atmosphere.\n\n"
    "The walls feature {wall_style}. "
    "The floor has {floor_pattern}. "
    "The lighting is {lighting}.\n\n"
    "In the center of the room, {focal_piece}. "
    "On the left wall, {left_furniture}. "
    "On the right wall, {right_furniture}.\n\n"
    "Small details like {decorative_details} complete the scene. "
    "No watermarks."
)


def build_prompt(
    room_type: str,
    art_style: str,
    mood: str,
    wall_style: str,
    floor_pattern: str,
    lighting: str,
    focal_piece: str,
    left_furniture: str,
    right_furniture: str,
    decorative_details: str | list[str],
) -> str:
    """
    Build a prompt string from individual options.

    Args:
        decorative_details: A single string or a list of detail strings.
                            If a list, items are joined with ', '.
    """
    if isinstance(decorative_details, list):
        decorative_details = ", ".join(decorative_details)

    return PROMPT_TEMPLATE.format(
        room_type=room_type,
        art_style=art_style,
        mood=mood,
        wall_style=wall_style,
        floor_pattern=floor_pattern,
        lighting=lighting,
        focal_piece=focal_piece,
        left_furniture=left_furniture,
        right_furniture=right_furniture,
        decorative_details=decorative_details,
    )


def random_prompt(n_details: int = 2) -> str:
    """
    Generate a prompt with randomly selected options.

    Args:
        n_details: How many decorative details to include (default 2).
    """
    s = OPTIONS["structural"]
    v = OPTIONS["visual"]

    return build_prompt(
        room_type=random.choice(s["room_type"]),
        art_style=random.choice(v["art_style"]),
        mood=random.choice(v["mood"]),
        wall_style=random.choice(s["wall_style"]),
        floor_pattern=random.choice(s["floor_pattern"]),
        lighting=random.choice(v["lighting"]),
        focal_piece=random.choice(s["focal_piece"]),
        left_furniture=random.choice(s["left_furniture"]),
        right_furniture=random.choice(s["right_furniture"]),
        decorative_details=random.sample(s["decorative_details"], k=n_details),
    )


def save_options_json(path: str = "isometric_options.json") -> None:
    """Save OPTIONS dict to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(OPTIONS, f, indent=2, ensure_ascii=False)
    print(f"Saved options to {path}")


# ──────────────────────────────────────────────
# EXAMPLE USAGE
# ──────────────────────────────────────────────

if __name__ == "__main__":

    # 1. Manual selection
    manual_prompt = build_prompt(
        room_type="bathroom",
        art_style="thick, clean, bold black outlines and a soft pastel color palette",
        mood="warm, Lo-Fi Cozy",
        wall_style="warm paneling with decorative vertical lines",
        floor_pattern="checkered tiles with a simple geometric pattern",
        lighting="soft diffused natural light from a small window",
        focal_piece=(
            "a prominent clawfoot bathtub with wooden feet and a plank tray "
            "holding a ceramic cup and a candle"
        ),
        left_furniture=(
            "a multi-level wooden shelf holds stacked towels, cosmetic bottles, "
            "and decorative jars, with fluffy slippers below"
        ),
        right_furniture=(
            "a wooden vanity cabinet with small legs, a sink basin, chrome faucet, "
            "and a rounded mirror with a flower accent above"
        ),
        decorative_details=[
            "a potted plant with large broad leaves",
            "a frog-shaped bath mat with a small crown",
        ],
    )

    print("── MANUAL PROMPT ──────────────────────────────")
    print(manual_prompt)

    print("\n── RANDOM PROMPT ──────────────────────────────")
    print(random_prompt(n_details=3))

    # 2. Save options to JSON
    save_options_json("isometric_options.json")