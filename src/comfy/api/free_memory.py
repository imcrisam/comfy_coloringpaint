import os
from typing import Optional

import requests


def free_memory(server_address: Optional[str] = None, timeout: float = 100.0, verbose: bool = False) -> bool:
    """Envía un único POST vacío a la ruta `/free` del servidor ComfyUI.

    - `server_address` puede incluir o no el esquema (http://).
    - Devuelve True si la petición responde con status 2xx.
    - Lanza excepción en caso de error o respuesta no 2xx.
    """
    if server_address is None:
        server_address = os.getenv("COMFY_SERVER_ADDRESS", "host.docker.internal:8188")

    if not server_address.startswith("http://") and not server_address.startswith("https://"):
        base = "http://" + server_address
    else:
        base = server_address

    url = base.rstrip("/") + "/free"

    if verbose:
        print(f"POST -> {url} (body: unload_models=true, free_memory=true)")

    try:
        resp = requests.post(url, json={"unload_models": True, "free_memory": True}, timeout=timeout)
        print(f"resp: {resp.status_code}")
    except Exception as exc:  # pragma: no cover - network/runtime errors
        if verbose:
            print(f"Error enviando POST a {url}: {exc}")
        raise

    if 200 <= resp.status_code < 300:
        if verbose:
            print(f"OK: {resp.status_code}")
        return True

    # Respuesta no exitosa
    raise RuntimeError(f"POST a {url} devolvió status {resp.status_code}: {resp.text}")


__all__ = ["free_memory"]
