from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from functools import lru_cache
from typing import Generator
import torch
import re
from services.prompt_builder import SYSTEM_PROMPT
from threading import Thread

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MAX_NEW_TOKENS = 150
MAX_INPUT_TOKENS = 400

@lru_cache(maxsize=1)
def load_model():
    print(f"[inference] loading {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float32,
        device_map="cpu",
        low_cpu_mem_usage=True,
    )
    model.eval()
    print("[inference] model ready")
    return tokenizer, model

def _stream_tokens(prompt: str) -> Generator[str, None, None]:
    """Core streaming function — yields words as model produces them."""
    tokenizer, model = load_model()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(
        text, return_tensors="pt",
        truncation=True, max_length=MAX_INPUT_TOKENS
    )

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )

    thread = Thread(
        target=model.generate,
        kwargs=dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.3,
        )
    )
    thread.start()

    buffer = ""
    for token_text in streamer:
        buffer += token_text
        while " " in buffer:
            word, buffer = buffer.split(" ", 1)
            if word.strip():
                yield word + " "

    if buffer.strip():
        yield buffer.strip()

    thread.join()

def generate_hint_stream(prompt: str) -> Generator[str, None, None]:
    """Streaming hint — yields words in real time."""
    yield from _stream_tokens(prompt)

def generate_hint(prompt: str) -> str:
    """Non-streaming hint — returns full text at once."""
    return clean_output("".join(_stream_tokens(prompt)))

def clean_output(text: str) -> str:
    for marker in ["hint:", "player_state:", "ctx_docs:", "---"]:
        if marker in text:
            text = text.split(marker)[-1]

    lines = text.strip().split("\n")
    clean_lines = [
        l for l in lines
        if not (l.count(":") > 3 and l.count(" ") > 5)
    ]
    text = " ".join(clean_lines).strip()

    sentences = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(sentences[:3]).strip()