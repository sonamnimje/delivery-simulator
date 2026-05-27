import os
import asyncio
import httpx
import json
from typing import Any
from pathlib import Path
from fastapi import HTTPException
from dotenv import load_dotenv
from app.prompts.prompt_builder import build_prompt
from app.utils.json_utils import extract_first_json
from app.models.schemas import DramaResponse

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def call_openrouter(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 1500,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()


async def generate_drama(situation: str, mood: str) -> Any:
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENROUTER_API_KEY is not set. Create backend/.env from .env.example and add your OpenRouter key.",
        )

    prompt = build_prompt(situation, mood)

    last_err = None
    for attempt in range(3):
        raw = await call_openrouter(prompt)
        # Try to extract content from known shapes
        text = None
        try:
            # OpenRouter likely returns choices -> message -> content
            if isinstance(raw, dict) and "choices" in raw:
                ch = raw.get("choices")[0]
                if isinstance(ch, dict) and "message" in ch:
                    text = ch["message"].get("content")
                else:
                    text = ch.get("text") or ch.get("content")
            elif isinstance(raw, dict) and "output" in raw:
                text = raw.get("output")
            else:
                text = json.dumps(raw)
        except Exception as e:
            text = json.dumps(raw)

        # Try parsing JSON
        try:
            parsed = extract_first_json(text)
            # Validate with pydantic
            drama = DramaResponse.model_validate(parsed)
            return drama
        except Exception as e:
            last_err = e
            # try to nudge the model by appending a clarifying system message
            prompt = prompt + "\n\nIf you didn't output valid JSON, output only the JSON now."
            await asyncio.sleep(1)

    raise RuntimeError(f"Failed to parse model response as JSON: {last_err}")


async def regenerate_scene(drama: dict, scene_index: int) -> Any:
    """Regenerate a single scene using the model. Returns a parsed scene dict."""
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENROUTER_API_KEY is not set. Create backend/.env from .env.example and add your OpenRouter key.",
        )

    # find the existing scene context
    existing_scenes = drama.get("scenes") if isinstance(drama, dict) else None
    scene_context = None
    if existing_scenes:
        for s in existing_scenes:
            if int(s.get("scene_index")) == int(scene_index):
                scene_context = s
                break

    prompt = build_prompt(regenerate_scene={"scene_index": scene_index, "scene_context": scene_context})

    last_err = None
    for attempt in range(3):
        raw = await call_openrouter(prompt)
        text = None
        try:
            if isinstance(raw, dict) and "choices" in raw:
                ch = raw.get("choices")[0]
                if isinstance(ch, dict) and "message" in ch:
                    text = ch["message"].get("content")
                else:
                    text = ch.get("text") or ch.get("content")
            else:
                text = json.dumps(raw)
        except Exception:
            text = json.dumps(raw)

        try:
            parsed = extract_first_json(text)
            # minimal validation: ensure scene_index matches
            if isinstance(parsed, dict) and int(parsed.get("scene_index", -1)) == int(scene_index):
                return parsed
            else:
                last_err = ValueError("Parsed scene did not match requested scene_index")
        except Exception as e:
            last_err = e
            prompt = prompt + "\n\nIf you didn't output valid JSON for the scene, output only the scene JSON now."
            await asyncio.sleep(1)

    raise RuntimeError(f"Failed to parse scene from model response: {last_err}")
