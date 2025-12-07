from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean
from app.database import Base


class Libro(Base):
    __tablename__ = "libro"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey("genre.id"), nullable=False)
    editor_id: Mapped[int] = mapped_column(Integer, ForeignKey("editorial.id"), nullable=False)
    avaible: Mapped[bool] = mapped_column(Boolean, default= True, nullable=False)
