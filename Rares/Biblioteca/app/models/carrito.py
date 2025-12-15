from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Carrito(Base):
    __tablename__ = "carritos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"))
    libro_id: Mapped[int] = mapped_column(Integer, ForeignKey("libro.id"))
    
    '''Relaciones de la tabla carritos
    1. Cada item de carrito apunta a un usuario
    2. Un item de carrito apunta a un libro
    '''
    
    usuario = relationship("Usuario", back_populates="orden_pedidos")
    libro = relationship("Libro", back_populates="orden_pedidos")
