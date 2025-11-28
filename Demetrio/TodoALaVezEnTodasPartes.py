# probando git
# modelos pydantic
from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session

app = FastAPI()

class Base(DeclarativeBase):
    pass

class Carrito(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int
    libro_id: int
    
class Usuario(BaseModel):  # solo hace validacion, no hay que hacer CRUD
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    password: str
    
# entradas AQLalchemy para las clases de usuario y carrito

class UsuarioORM(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(40), nullable=False)
    
class CarritoORM(Base):
    __tablename__ = "carrito"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    libro_id: Mapped[int] = mapped_column(Integer, nullable=False)
   
# api rest: peticiones CRUD para carrito
# ver carrito GET /1
# !! NO !! hay que crear carrito por que cada usuario ya tiene uno
# añadir libro a carrito POST /2
# quitar libro de carrito DELETE /3
# !! NO !! hay que actualizar total o parcialmente carrito, no hay UPDATE o PATCH aqui

@app.get("/", response_model=Carrito) #/1
def ver_carrito(db: Session = Depends(get_db)):
    # db.execute(): ejecuta la consulta
    # select(Song): crea consulta SELECT * FROM song
    # .scalars(): extrae los objetos Song
    # .all(): obtiene los resultados como lista
    return db.execute(select("carrito")).scalars().all()
# falta bbdd para mostrar el carrito del usuario activo

@app.post("/") #/2
def añadir_libro_carrito():
    pass

@app.delete("/") #/3
def borrar_libro_carrito():
    pass