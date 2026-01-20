import requests

OLLAMA_HOST = "http://192.168.1.81:11434"
MODEL_NAME = "olmo-3:latest"

def call_llm(prompt: str, temperature: float = 0.2, max_tokens: int = 6000) -> str:
    url = f"{OLLAMA_HOST}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "think": False
        }
    }

    response = requests.post(url, json=payload, timeout=180)
    print("OLLAMA STATUS:", response.status_code)
    print("OLLAMA RAW TEXT:", response.text[:1500])

    response.raise_for_status()
    data = response.json()

    # ✅ fallback if response is empty
    text = (data.get("response") or "").strip()
    if not text:
        text = (data.get("thinking") or "").strip()

    return text
