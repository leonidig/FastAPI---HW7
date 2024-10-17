from sqlalchemy.orm import Mapped
from .. import Base


class Movie(Base):
    __tablename__ = "movies"
    title: Mapped[str]
    director: Mapped[str]
    release_year: Mapped[int]
    rating: Mapped[float]