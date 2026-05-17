from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.models.schemas import GenerateRequest, DramaResponse
from app.services.llm_service import generate_drama, regenerate_scene

router = APIRouter()


@router.post("/generate", response_model=DramaResponse)
async def generate(req: GenerateRequest):
    try:
        result = await generate_drama(req.situation, req.mood)
        return result
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/regenerate-scene")
async def regenerate_scene_route(payload: dict):
    """Regenerate a single scene. Expects payload: { drama: <existing drama dict>, scene_index: int }"""
    try:
        drama = payload.get("drama")
        scene_index = int(payload.get("scene_index"))
        new_scene = await regenerate_scene(drama, scene_index)
        return {"scene": new_scene}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
