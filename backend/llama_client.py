import requests
import time
import re

OLLAMA_HOST = "http://192.168.1.81:11434"
MODEL_NAME = "olmo-3:latest"

def has_all_sections(text: str) -> bool:
    required = [f"{i})" for i in range(1, 13)]
    return all(r in text for r in required)

def find_missing_sections(text: str):
    missing = []
    for i in range(1, 13):
        if f"{i})" not in text:
            missing.append(i)
    return missing

def call_llm(prompt: str, temperature: float = 0.05, max_tokens: int = 16000, retries: int = 3) -> str:
    url = f"{OLLAMA_HOST}/api/generate"

    full_text = ""
    current_prompt = prompt

    for attempt in range(retries):
        payload = {
            "model": MODEL_NAME,
            "prompt": current_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": 0.9,
                "repeat_penalty": 1.15,
                "num_ctx": 16384,   # 🔥 increase if supported
            }
        }

        response = requests.post(url, json=payload, timeout=900)
        response.raise_for_status()
        data = response.json()

        text = (data.get("response") or "").strip()
        if not text:
            text = (data.get("thinking") or "").strip()

        full_text += "\n" + text

        if has_all_sections(full_text):
            return full_text.strip()

        missing = find_missing_sections(full_text)
        print(f"Attempt {attempt+1}: Missing sections {missing}")

        # ask model to continue from the first missing section
        first_missing = missing[0] if missing else 12
        current_prompt = (
            prompt
            + "\n\nYou stopped early. Continue output from section "
            + f"{first_missing}) ONLY. Do not repeat earlier sections.\n"
        )

        time.sleep(0.5)

    return full_text.strip()
