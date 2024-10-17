from typing import Optional
from pydantic import BaseModel, ConfigDict


class MovieData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int]
    title: str
    director: str
    release_year: int
    rating : float


class DeleteMovie(BaseModel):
    director: str
    movie_id: int


class DeleteResponse(BaseModel):
    message: str