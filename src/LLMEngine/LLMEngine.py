# OllamaLoader.py

import requests
from typing import Literal

llama_cpp_available = False

class LLMEngine:
    def __init__(self, model_name="mistral", backend: Literal["ollama", "llama"] = "ollama", model_path=None, gpu_layers=0):
        self.backend = backend

        if backend == "ollama":
            self.model_name = model_name
            self.api_url = "http://localhost:11434/api/generate"

        elif backend == "llama":
            if not llama_cpp_available:
                raise ImportError("llama-cpp-python is not installed. Please install it via pip.")

            if not model_path:
                raise ValueError("model_path must be specified when using llama backend")

            self.llm = Llama(model_path=model_path, n_gpu_layers=gpu_layers, n_ctx=4096, n_threads=6)

        else:
            raise ValueError(f"Unsupported backend: {backend}")

    def generate(self, prompt: str) -> str:
        if self.backend == "ollama":
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

        elif self.backend == "llama":
            result = self.llm(prompt, max_tokens=512, stop=["</s>", "###"])
            return result["choices"][0]["text"].strip()

        else:
            raise RuntimeError("Invalid backend configured")
