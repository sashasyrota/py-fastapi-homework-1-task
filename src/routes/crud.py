from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import MovieModel
from src.schemas.movies import MovieCreateSchema


async def get_movies(db: AsyncSession, page: int, per_page: int):
    stmt = select(MovieModel)
    result = await db.execute(stmt)
    result = result.scalars().all()
    return result


async def create_movie(movie_schema: MovieCreateSchema, db: AsyncSession):
    movie_db = MovieModel(
        name=movie_schema.name,
        date=movie_schema.date,
        score=movie_schema.score,
        genre=movie_schema.genre,
        overview=movie_schema.overview,
        crew=movie_schema.crew,
        orig_title=movie_schema.orig_title,
        status=movie_schema.status,
        orig_lang=movie_schema.orig_lang,
        budget=movie_schema.budget,
        revenue=movie_schema.revenue,
        country=movie_schema.country,
    )
    db.add(movie_db)
    await db.commit()
    return movie_db


async def get_movie(movie_id: int, db: AsyncSession):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    result = result.scalar()
    return result
