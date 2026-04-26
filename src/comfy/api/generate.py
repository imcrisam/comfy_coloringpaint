from pprint import pprint
from typing import Dict, Any
import uuid

import requests
import time

import json
import websocket
class SimpleComfyGenerator:


    def __init__(self, server_address: str = "host.docker.internal:8188"):
        self.server_address = server_address
        self.base_url = f"http://{server_address}"
        self.client_id = str(uuid.uuid4())

    # --- comunicación básica con ComfyUI ---------------------------------
    def queue_prompt(self, prompt: Dict[str, Any]) -> str:
        resp = requests.post(f"{self.base_url}/prompt", json={"prompt": prompt, "client_id": self.client_id})
        resp.raise_for_status()
        return resp.json().get("prompt_id")

    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/history/{prompt_id}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    def wait_for_completion(
        self, prompt_id: str, timeout: int = 300, interval: int = 2
    ) -> Dict[str, Any]:
        start = time.time()
        while time.time() - start < timeout:
            hist = self.get_history(prompt_id)
            if prompt_id in hist:
                return hist[prompt_id]
            time.sleep(interval)
        raise TimeoutError("Timeout waiting for completion")

    def listen_ws(self, prompt_id: str, nodes_to_wait: list = None):
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
        try:
            while True:
                
                hist = self.get_history(prompt_id)
                if prompt_id in hist:
                    return
                
                msg = ws.recv()
                try:
                    data = json.loads(msg)
                except:
                    continue

                msg_type = data.get("type")
                msg_data = data.get("data", {})
                
             
                if msg_type == "crystools.monitor":
                    continue
                
                if msg_data.get("prompt_id") != prompt_id:
                    continue

                pprint(f"Mensaje WS recibido: {msg_type} - {msg_data.get('node', '')}")
                if msg_type == "executing":
                    node = msg_data.get("node")
                    print(f"▶ Ejecutando nodo {node}")

                if nodes_to_wait and msg_data.get("node") not in nodes_to_wait:
                    continue

                elif msg_type == "execution_error":
                    raise RuntimeError(msg_data.get("exception"))

                elif msg_type == "executed":
                    
                    if nodes_to_wait and msg_data.get("node") in nodes_to_wait:
                        nodes_to_wait.remove(msg_data.get("node"))
                        pprint(msg_data)
                        pprint(f"Nodo completado: {msg_data.get('node')}. Restantes: {nodes_to_wait}")
                        if not nodes_to_wait:
                            return
                        continue
                    
                    print(f"✅ Nodo completado: {msg_data.get('node')}")
                    print("✅ Prompt terminado")
                    return


        finally:
            ws.close()
            time.sleep(3)  # Esperar un momento para asegurar que la conexión se cierre correctamente
            

__all__ = ["SimpleComfyGenerator"]
