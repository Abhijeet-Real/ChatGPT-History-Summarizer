# OllamaLoader.py

import requests

class LLMEngine:
    def __init__(self, model_name="mistral", host="http://localhost:11434"):
        self.model_name = model_name
        self.api_url = f"{host}/api/generate"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.api_url,
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.text}")
        return response.json()["response"].strip()
