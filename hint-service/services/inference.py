from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import lru_cache
from typing import Generator
import torch
import re
from services.prompt_builder import SYSTEM_PROMPT

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
MAX_NEW_TOKENS = 100
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

def generate_hint(prompt: str) -> dict:
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
        truncation=True, max_length=500
    )

    input_token_count = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.3,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    output_token_count = len(new_tokens)
    raw  = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    hint = clean_output(raw)

    return {
        "hint": hint,
        "usage": {
            "input_tokens":  input_token_count,
            "output_tokens": output_token_count,
            "total_tokens":  input_token_count + output_token_count,
        }
    }

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

def generate_hint_stream(prompt: str) -> Generator[str, None, None]:
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
        truncation=True, max_length=500
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.3,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    raw  = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    hint = clean_output(raw)

    for word in hint.split(" "):
        if word.strip():
            yield word + " "