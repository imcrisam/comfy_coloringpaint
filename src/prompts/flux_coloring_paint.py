def build_prompt(location: str, sub_location: str, theme: str) -> str:
    """Build the image generation prompt from the 3 scene values and a theme."""
    return (
        f"Isometric miniature illustration of a {sub_location} inside a {location}, "
        f"thick black outlines, bold clean linework, flat cell shading, "
        f"{theme} theme, highly detailed, white background, "
        f"no blur, no watercolor, no thin lines"
    )