from groq import Groq
import os
import re
from typing import Generator
from services.prompt_builder import SYSTEM_PROMPT

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL_ID = "llama-3.3-70b-versatile"

def generate_hint_stream(prompt: str) -> Generator[str, None, None]:
    stream = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=120,
        temperature=0.7,
        stream=True,
    )

    buffer = ""
    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        buffer += token
        while " " in buffer:
            word, buffer = buffer.split(" ", 1)
            if word.strip():
                yield word + " "

    if buffer.strip():
        yield buffer.strip()

def generate_hint(prompt: str) -> str:
    return "".join(generate_hint_stream(prompt))