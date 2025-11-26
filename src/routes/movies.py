from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, MovieModel
from schemas.movies import PaginatedMovies


router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=PaginatedMovies)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MovieModel))
    all_movies = result.scalars().all()
    total_items = len(all_movies)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    movies_page = all_movies[start:end]

    prev_page = f"movies/?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = f"movies/{page+1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies_page,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}", response_model=MovieModel)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().one()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
