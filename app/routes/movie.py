from typing import List
from sqlalchemy import select
from db import Session, Movie
from schemas import MovieData, DeleteMovie, DeleteResponse
from main import app
from fastapi import HTTPException


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/movies", response_model=List[MovieData])
def get_all_movies():
    with Session.begin() as session:
        movies = session.scalars(select(Movie)).all()
        movies = [MovieData.model_validate(movie) for movie in movies]
        return movies
    

@app.post("/movies", response_model=MovieData)
def create_movie(data: MovieData):
    with Session.begin() as session: 
        movie = Movie(**data.model_dump())
        session.add(movie)
        return MovieData.model_validate(movie)
    

@app.get("/movie_info/{movie_id}", response_model=MovieData)
def movie_info(movie_id: int):
    with Session.begin() as session:
        selected_post = session.scalar(select(Movie).where(Movie.id == movie_id))
        if selected_post is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        else: 
            selected_movie = MovieData.model_validate(selected_post)
            return selected_movie



@app.delete("/delete_movie/{movie_id}", response_model=DeleteResponse)
def delete_movie(data: DeleteMovie):
    with Session.begin() as session:
        movie_to_delete = session.scalar(select(Movie).where(Movie.id == data.movie_id))
        if not movie_to_delete:
            raise HTTPException(status_code=404, detail="Movie not found")
        elif movie_to_delete.director != data.director:
            raise HTTPException(status_code=403, detail="You are not the author of this movie")
        session.delete(movie_to_delete)
        return DeleteResponse(message="Movie deleted successfully")
