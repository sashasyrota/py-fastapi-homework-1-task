from contextlib import asynccontextmanager
from urllib.request import Request

from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from src.database import init_db, close_db
from src.routes import movie_router
from src.routes.movies import InvalidValueError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Movies homework", description="Description of project", lifespan=lifespan
)


@app.exception_handler(InvalidValueError)
async def validation_exception_handler(request: Request, exc: InvalidValueError):
    raise HTTPException(
        status_code=422,
        detail=[
            {
                "loc": ["query", exc.name],
                "msg": "Input should be greater than or equal to 1",
                "type": "value_error.number.not_ge",
            }
        ],
    )


api_version_prefix = "/api/v1"

app.include_router(
    movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"]
)
