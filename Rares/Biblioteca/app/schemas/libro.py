from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

from genero import GenreRead

model_config = ConfigDict(from_attributes=True)

'''La importación del esquema de genero
se usará para la clase LibroFull'''

# Se aplicará la clase base con validadores como en UsuarioValido

class LibroBase(BaseModel):
    title: str
    price: float
    description: str
    genre_id: int

class LibroValido(BaseModel):
    model_config = model_config
    
    @field_validator("title")
    @classmethod
    def titulo_valido(cls, a: str | None) -> str | None:
        if a is None:
            return None
        
        titulo_decidido = a.strip()
        if not titulo_decidido:
            raise ValueError("El campo título no puede estar vacío.")
        return titulo_decidido
    
    @field_validator("price")
    @classmethod
    def precio_valido(cls, b: float | None) -> float | None:
        if b is None:
            return None
        
        if b <= 0.00:
            raise ValueError("El precio debe ser un número positivo.")
        return b

class LibroCreate(LibroBase, LibroValido):
    pass

class LibroRead(LibroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class LibroFull(LibroRead):
    genero: GenreRead

class LibroUpdate(BaseModel):
    pass

class LibroPatch(LibroValido):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    genre_id: Optional[int] = None

