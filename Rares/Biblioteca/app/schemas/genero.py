from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
from typing import Optional

model_config = ConfigDict(from_attributes=True)

'''Para hacer el esquema de Usuarios es obligatorio
establecer los validadores para email y la contraseña.'''

class UsuarioValido(BaseModel):
    model_config = model_config
    
    @field_validator("email")
    @classmethod
    def validar_email(cls, x: EmailStr | None) -> EmailStr | None:
        if x is None:
            return None
        
        if not x or not str(x).strip():
            raise ValueError("Si al usuario quieres registrar, el campo del email tendrás que rellenar.")
        
        return str(x).strip()
    
    @field_validator("password")
    @classmethod
    def validar_contrasena(cls, y: str | None) -> str | None:
        if y is None:
            return None
        
        if len(y) < 8:
            raise ValueError("La contraseña debe tener como mínio 8 caracteres.")
        
        return y

class UsuarioCreate(UsuarioValido):
    email: EmailStr
    password: str

class UsuarioResponse(BaseModel):
    
    # El campo password no está incluido en esta clase
    model_config = model_config
    
    id: int
    email: EmailStr

class UsuarioUpdate(UsuarioCreate):
    pass

class UsuarioPatch(UsuarioValido):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
