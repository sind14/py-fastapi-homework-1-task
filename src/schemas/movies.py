from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class MovieBase(BaseModel):
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


    class Config:
        orm_mode = True


class PaginatedMovies(BaseModel):
    movies: List[MovieBase]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
