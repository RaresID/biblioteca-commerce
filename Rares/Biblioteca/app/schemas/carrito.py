from pydantic import BaseModel, ConfigDict, field_validator
from usuario import UsuarioResponse
from libro import LibroRead

class CarritoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int
    libro_id: int
    
    @field_validator("id")
    @classmethod
    def validacion_id(cls, x: int) -> int:
        if x <= 0:
            raise ValueError("El ID del carrito debe ser un número positivo.")
        return x

class CarritoFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id:int
    usuario: UsuarioResponse
    libro: LibroRead

class CarritoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    usuario_id: int
    libro_id: int
