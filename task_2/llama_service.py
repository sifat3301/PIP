import json
import requests


class LLaMAWrapper:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @property
    def _llm_type(self) -> str:
        return "llama"

    def _call(self, prompt: str) -> str:
        response = requests.post(
            self.endpoint,
            json={"model": "llama2", "prompt": prompt, "max_tokens": 512},
            stream=True  # allows iter_lines
        )

        output_chunks = []
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    output_chunks.append(data["response"])
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                continue

        return "".join(output_chunks)
