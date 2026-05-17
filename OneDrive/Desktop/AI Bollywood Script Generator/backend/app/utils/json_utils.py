import re
import json


def extract_first_json(text: str) -> str:
    # Find first JSON object in a string
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidate = match.group(0)
        # try to balance braces if truncated
        # quick attempt: try incremental trimming until json.loads works
        for i in range(len(candidate), 0, -1):
            try:
                return json.loads(candidate[:i])
            except Exception:
                continue
    # fallback: attempt full parse
    try:
        return json.loads(text)
    except Exception:
        raise ValueError("Could not extract JSON from model response")
