from workflows._load_workflow import load_workflow

def build(
    prompts: list[str],
    outputs: list[str],
    width: int = 512,
    height: int = 512,
    format: str = "png",
    quality: int = 95,
) -> tuple[dict, list[str]]:
    """
    Construye una copia del workflow con los parámetros dados.

    Args:
        prompts:   Lista de prompts. Se unen con '-----' en el nodo 151.
        outputs:   Lista de rutas de salida. Se unen con '-----' en el nodo 156.
        width:     Ancho de la imagen de referencia (nodo 148).
        height:    Alto de la imagen de referencia (nodo 148).
        format:    Formato de salida ('png', 'jpg', etc.).
        quality:   Calidad de compresión (0–100).

    Returns:
        (workflow_modificado, output_node_ids)
        output_node_ids: lista de IDs de nodos SaveImageToPath.
    """
    wf = load_workflow("workflow_coloringpaint.json", "flux_2_coloringpaint")  # Carga el workflow base
    sep = "-----"

    # --- Prompts (nodo 151) ---
    wf["151"]["inputs"]["value"] = sep.join(prompts)

    # --- Rutas de salida (nodo 156) ---
    wf["156"]["inputs"]["value"] = sep.join(outputs)

    # --- Tamaño (nodo 148 → EmptyImage) ---
    wf["148"]["inputs"]["width"] = width
    wf["148"]["inputs"]["height"] = height

    # --- Formato y calidad en todos los SaveImageToPath ---
    output_node_ids = []
    for node_id, node in wf.items():
        if node.get("class_type") == "SaveImageToPath":
            node["inputs"]["format"] = format
            node["inputs"]["quality"] = quality
            output_node_ids.append(node_id)

    return wf, output_node_ids
