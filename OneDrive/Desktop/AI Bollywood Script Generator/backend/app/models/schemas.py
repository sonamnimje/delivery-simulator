from typing import List
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    situation: str
    mood: str = Field(default="Bollywood Masala")


class Dialogue(BaseModel):
    character: str
    line: str


class Scene(BaseModel):
    scene_index: int
    scene_title: str
    mood: str
    scene_description: str
    dialogues: List[Dialogue]


class Character(BaseModel):
    name: str
    role: str
    description: str


class DramaResponse(BaseModel):
    movie_title: str
    tagline: str
    characters: List[Character]
    scenes: List[Scene]
