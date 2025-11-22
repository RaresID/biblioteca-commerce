from sqlalchemy import Integer, String, Boolean, Column, Float
from app.database import Base

class libro(Base):
    __tablename__ = "libros"
    
    # Clave primaria del libro
    libro_id = Column(Integer, primary_key=True, nullable=False,index=True)
    titulo = Column(String, nullable=False)
    genero_id = Column(Integer, nullable=False)
    numero_paginas = Column(Integer,nullable=False)
    autor = Column(String, nullable=False)
    disponible = Column(Boolean,default=True)
    editora_id = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    
    