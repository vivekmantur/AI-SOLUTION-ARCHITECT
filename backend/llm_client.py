import os
import time
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"
   # or llama-3.1-8b-instant

def has_all_sections(text: str) -> bool:
    required = [f"{i})" for i in range(1, 13)]
    return all(r in text for r in required)

def find_missing_sections(text: str):
    return [i for i in range(1, 13) if f"{i})" not in text]

def call_llm(prompt: str, temperature: float = 0.05, max_tokens: int = 16000, retries: int = 3) -> str:
    full_text = ""
    current_prompt = prompt

    for attempt in range(retries):
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": current_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.9
        )

        text = (resp.choices[0].message.content or "").strip()
        full_text += "\n" + text

        if has_all_sections(full_text):
            return full_text.strip()

        missing = find_missing_sections(full_text)
        print(f"Attempt {attempt+1}: Missing sections {missing}")

        first_missing = missing[0] if missing else 12
        current_prompt = (
            prompt
            + f"\n\nYou stopped early. Continue output from section {first_missing}) ONLY. "
              "Do not repeat earlier sections.\n"
        )

        time.sleep(0.5)

    return full_text.strip()
