"""
Configuración de la aplicación FastAPI
"""

from fastapi import FastAPI
from app.database import init_db
from app.routers.api import router as api_router
from app.routers.web import router as web_router

from app.routers.api.libro import router as libro_router
from app.routers.api.genero import router as genero_router
from app.routers.api.carrito import router as carrito_router

# crea la instancia de la aplicación FastAPI
app = FastAPI(title="Librerías Demetrio", version="1.0.0")

# inicializa la base de datos con canciones por defecto
init_db()

# registrar los routers
app.include_router(api_router)
app.include_router(web_router)

app.include_router(libro_router)
app.include_router(genero_router)
app.include_router(carrito_router)

"""
# endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la página de Librería Demetrio"}
"""
