from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from .database import Base


class Libro(Base):
    __tablename__ = "libro"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    editor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, nullable=False)

