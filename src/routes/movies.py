import math
from urllib.request import Request
from xml.dom import ValidationErr

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.database.session import get_db
from . import crud
from ..schemas.movies import MovieListResponseSchema, MovieCreateSchema

router = APIRouter()


class InvalidValueError(Exception):
    def __init__(self, name):
        self.name = name


def get_page_url(page: int, per_page: int):
    return f"/theater/movies/?page={page}&per_page={per_page}"


@router.get("/movies/", tags=["movies"])
async def read_movies(
    db: AsyncSession = Depends(get_db), page: int = 1, per_page: int = 10
):
    if per_page < 1:
        raise InvalidValueError(name="per_page")
    if page < 1:
        raise InvalidValueError(name="page")

    movies_list = await crud.get_movies(db=db, page=page, per_page=per_page)
    offset = (page - 1) * per_page
    limit = per_page
    movies_list_query = movies_list[offset : offset + limit]
    if not movies_list_query:
        raise HTTPException(detail="No movies found.", status_code=404)
    total_items = len(movies_list)
    prev_page_url = None
    if page > 1:
        prev_page_url = get_page_url(page=page - 1, per_page=per_page)
    total_pages = math.ceil(total_items / per_page)
    next_page_url = None
    if page + 1 <= total_pages:
        next_page_url = get_page_url(page=page + 1, per_page=per_page)
    result = {
        "movies": movies_list_query,
        "prev_page": prev_page_url,
        "next_page": next_page_url,
        "total_pages": total_pages,
        "total_items": total_items,
    }
    return result


@router.post("/movies/", tags=["movies"], response_model=MovieListResponseSchema)
async def create_movie(
    movie_schema: MovieCreateSchema, db: AsyncSession = Depends(get_db)
):
    result = await crud.create_movie(movie_schema=movie_schema, db=db)
    return result


@router.get("/movies/{movie_id}/", tags=["movies"])
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_movie(movie_id=movie_id, db=db)
    if not result:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return result
