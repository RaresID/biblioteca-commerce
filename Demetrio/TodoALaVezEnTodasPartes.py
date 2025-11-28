# probando git
# modelos pydantic
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Carrito(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    
class Usuario(BaseModel):
    id: int
    email: str
    password: str
    