import os
import time
from groq import Groq

# Initialize Groq client using API key from environment variable
# Make sure GROQ_API_KEY is set in your environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LLM model to use
# You can switch to a smaller/faster model if needed
MODEL_NAME = "openai/gpt-oss-120b"
# Alternative example:
# MODEL_NAME = "llama-3.1-8b-instant"

# Total number of tasks expected in the LLM output
TOTAL_TASKS = 7


def has_all_tasks(text: str) -> bool:
    """
    Check whether the output text contains ALL required task markers.

    Expected format:
    TASK 1
    TASK 2
    ...
    TASK 7
    """
    required = [f"TASK {i}" for i in range(1, TOTAL_TASKS + 1)]
    return all(r in text for r in required)


def find_missing_tasks(text: str):
    """
    Identify which task numbers are missing from the LLM output.

    Returns:
        List of missing task numbers (e.g., [3, 5])
    """
    return [i for i in range(1, TOTAL_TASKS + 1) if f"TASK {i}" not in text]


def call_llm(
    prompt: str,
    temperature: float = 0.05,
    max_tokens: int = 16000,
    retries: int = 3
) -> str:
    """
    Calls the LLM and ensures all required TASK outputs are generated.

    If the model stops early, it:
    - Detects missing tasks
    - Re-prompts the model to continue from the first missing task
    - Retries up to the specified number of times

    Args:
        prompt: Initial prompt sent to the LLM
        temperature: Controls randomness (lower = more deterministic)
        max_tokens: Max tokens per response
        retries: Number of retry attempts if output is incomplete

    Returns:
        Combined LLM output containing all tasks (if successful)
    """

    # Accumulates full response across retries
    full_text = ""

    # Prompt that will be sent to the model
    current_prompt = prompt

    for attempt in range(retries):
        # Call Groq chat completion API
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": current_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.9
        )

        # Extract and clean response text
        text = (resp.choices[0].message.content or "").strip()

        # Append response if not empty
        if text:
            full_text += "\n" + text

        # If all tasks are present, return final output
        if has_all_tasks(full_text):
            return full_text.strip()

        # Otherwise, identify missing tasks
        missing = find_missing_tasks(full_text)
        print(f"Attempt {attempt + 1}: Missing tasks {missing}")

        # Determine where the model stopped
        first_missing = missing[0] if missing else TOTAL_TASKS

        # Ask the model to continue ONLY from the missing task
        current_prompt = (
            prompt
            + f"\n\nYou stopped early. Continue output from TASK {first_missing} ONLY. "
              "Do not repeat earlier tasks. "
              "Follow the exact same output format.\n"
        )

        # Small delay to avoid rate limits or burst failures
        time.sleep(0.5)

    # Return whatever was generated after all retries
    return full_text.strip()
