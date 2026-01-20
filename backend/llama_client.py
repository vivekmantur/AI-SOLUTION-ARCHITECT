import requests
from dotenv import load_dotenv


load_dotenv()

# Use your actual Ollama server (LAN or local machine)
OLLAMA_HOST = "http://192.168.1.81:11434"
MODEL_NAME = "llama3"

def call_llama(prompt: str, temperature: float = 0.2, max_tokens: int = 2048) -> str:
    """
    Calls Ollama LLM using JSON mode for reliable output.
    Returns the generated content or an error message.
    """
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a senior cloud solution architect. "
                           "Always reply in valid JSON ONLY. "
                           "Do not use markdown or natural language. "
                           "Return pure JSON object."
            },
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "format": "json",              # <--- IMPORTANT for structured JSON output
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens, # <--- Allows longer valid JSON
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # Extract generated text content
        return data["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return "ERROR: Unable to reach Ollama. Is it running?"

    except requests.exceptions.Timeout:
        return "ERROR: Ollama response timeout. Try reducing complexity or increasing timeout."

    except Exception as e:
        print(f"❌ Ollama LLM Error: {e}")
        return f"ERROR: {str(e)}"
