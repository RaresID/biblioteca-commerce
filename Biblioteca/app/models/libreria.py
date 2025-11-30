from sqlalchemy import Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base

class libro(Base):
    __tablename__ = "libros"
    
    # Clave primaria del libro
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    titulo: Mapped[str] = mapped_column(String(75), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False) 
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    #ID editora y genero son claves ajenas
    editora_id: Mapped[int] = mapped_column(Integer, ForeignKey("editores.editora_id"))
    genero_id: Mapped[int] = mapped_column(Integer, ForeignKey("genero.genero_id"))
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)

    # Relaciones de la clase Libro
    
    '''Primera relación: Una editora a varios libros'''
    edit: Mapped["editora"] = relationship(back_populates="libros")
    genre: Mapped["genero"] = relationship(back_populates="libros")
    
class editora(Base):
    __tablename__ = "editores"
    
    editora_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    idioma: Mapped[str] = mapped_column(String(50), nullable=False)
    origen: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Relación de muchos libros a una sola editora
    lista_libros: Mapped[list["libro"]] = relationship(back_populates="editora")

class genero(Base):
    __tablename__ = "generos_literarios"
    
    genero_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_genero: Mapped[str] = mapped_column(String(75), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(150), nullable=False)
    
    # Relación muchos libros en un género
    lista_libros: Mapped[list["libro"]] = relationship(back_populates="genero")

# A continuación se establece la estructura para el usuario
class usuario(Base):
    __tablename__ = "usuarios"
    
    usuario_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(40), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
class carrito(Base):
    __tablename__ = "carritos"
    
    carrito_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
class item_carr(Base):
    __tablename__ = "item_caritos"
    
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    libro_id: Mapped[int] = mapped_column(Integer, ForeignKey("libros.id"))
    carrito_id: Mapped[int] = mapped_column(Integer, ForeignKey("carritos.carrito_id"))
    
