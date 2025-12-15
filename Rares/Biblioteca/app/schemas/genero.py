from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

model_config = ConfigDict(from_attributes=True)

class GenreBase(BaseModel):
    name: str

class GenreValido(BaseModel):
    model_config = model_config
    
    name: Optional[str] = None
    
    @field_validator("name")
    @classmethod
    def nombre_valido(cls, a: str | None) -> str | None:
        if a is None:
            return None
        nombre_decidido = a.strip()
        if not nombre_decidido:
            raise ValueError("El nombre del género no debe estar vacío.")
        return nombre_decidido

class GenreCreate(GenreBase,GenreValido):
    pass

class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class GenreUpdate(GenreCreate):
    pass
