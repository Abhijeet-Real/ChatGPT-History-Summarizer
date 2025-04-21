from llama_cpp import Llama

class LLMEngine:
    def __init__(self, model_path, ctx=8192, threads=6, gpu_layers=0):
        print(f"🚀 Initializing LLM (GPU layers: {gpu_layers})")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=ctx,
            n_threads=threads,
            n_gpu_layers=gpu_layers
        )

    def generate(self, prompt, max_tokens=512):
        result = self.llm(prompt, max_tokens=max_tokens)
        return result["choices"][0]["text"].strip()
