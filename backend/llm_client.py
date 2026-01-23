import os
import time
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"
# or "llama-3.1-8b-instant"


TOTAL_TASKS = 7


def has_all_tasks(text: str) -> bool:
    required = [f"TASK {i}" for i in range(1, TOTAL_TASKS + 1)]
    return all(r in text for r in required)


def find_missing_tasks(text: str):
    return [i for i in range(1, TOTAL_TASKS + 1) if f"TASK {i}" not in text]


def call_llm(
    prompt: str,
    temperature: float = 0.05,
    max_tokens: int = 16000,
    retries: int = 3
) -> str:
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
        if text:
            full_text += "\n" + text

        if has_all_tasks(full_text):
            return full_text.strip()

        missing = find_missing_tasks(full_text)
        print(f"Attempt {attempt + 1}: Missing tasks {missing}")

        first_missing = missing[0] if missing else TOTAL_TASKS

        current_prompt = (
            prompt
            + f"\n\nYou stopped early. Continue output from TASK {first_missing} ONLY. "
              "Do not repeat earlier tasks. "
              "Follow the exact same output format.\n"
        )

        time.sleep(0.5)

    return full_text.strip()
