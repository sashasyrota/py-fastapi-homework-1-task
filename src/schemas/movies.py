import datetime

from pydantic import BaseModel, Field, ConfigDict


class MovieBaseSchema(BaseModel):
    name: str = Field(max_length=255)
    date: datetime.datetime
    score: int
    genre: str = Field(max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(max_length=255)
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float
    country: str = Field(max_length=3)


class MovieListResponseSchema(MovieBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class MovieCreateSchema(MovieBaseSchema):
    pass
