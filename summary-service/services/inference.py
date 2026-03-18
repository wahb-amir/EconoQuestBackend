from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import lru_cache
import torch
import json
import re

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MAX_NEW_TOKENS = 80   # was 300 — one sentence output only now

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

def generate_round_summary(round_num: int, state: dict) -> str:
    tokenizer, model = load_model()

    # single round — tiny prompt, tiny output
    prompt = (
        f"Round {round_num} results: "
        f"GDP={state.get('gdp')}% Inflation={state.get('inf')}% "
        f"Unemployment={state.get('unemp')}% Debt={state.get('dbt')}% "
        f"Mood={state.get('mood')} Innovation={state.get('inn')} "
        f"Currency={state.get('cur')} Printed={'yes' if state.get('prt') else 'no'}. "
        f"Write one sentence describing the key economic outcome this round."
    )

    messages = [
        {
            "role": "system",
            "content": "You are a concise economic analyst. Respond in exactly one sentence."
        },
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(
        text, return_tensors="pt",
        truncation=True, max_length=200  # tiny input
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,      # greedy
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2,
            # removed top_p and top_k — incompatible with do_sample=False
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    raw = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    # cap at 1 sentence
    sentences = re.split(r"(?<=[.!?])\s+", raw)
    return sentences[0].strip() if sentences else raw