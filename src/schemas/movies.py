from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genres: List[str]
    overview: str
    crew: List[str]
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

    @field_validator("genres", mode="before")
    @classmethod
    def split_genres(cls, v):
        if isinstance(v, str):
            return [g.strip() for g in v.split(",")]
        return v

    @field_validator("crew", mode="before")
    @classmethod
    def split_crew(cls, v):
        if isinstance(v, str):
            return [c.strip() for c in v.split(",")]
        return v

    class Config:
        orm_mode = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
