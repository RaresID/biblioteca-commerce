from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.database import Base

class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    libros = relationship(
        "Libro",
        back_populates="genero"
    )
