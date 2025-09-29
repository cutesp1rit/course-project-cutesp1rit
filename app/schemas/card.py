from typing import Optional

from pydantic import BaseModel, Field


class CardCreate(BaseModel):
    deck_id: int
    front: str = Field(min_length=1, max_length=500)
    back: str = Field(min_length=1, max_length=2000)


class CardUpdate(BaseModel):
    front: Optional[str] = Field(default=None, min_length=1, max_length=500)
    back: Optional[str] = Field(default=None, min_length=1, max_length=2000)


class CardOut(BaseModel):
    id: int
    deck_id: int
    front: str
    back: str
