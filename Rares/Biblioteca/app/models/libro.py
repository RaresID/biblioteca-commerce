from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from app.database import Base


class Libro(Base):
    __tablename__ = "libro"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey("genre.id"), nullable=False)
    
    genero = relationship(
        "Genre",
        back_populates="libros"
    )
    
    orden_pedidos = relationship(
        "Carrito",
        back_populates="libro"
    )
