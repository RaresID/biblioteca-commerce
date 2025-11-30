# main.py

from fastapi import FastAPI
from database import engine, Base # Importa el motor y la clase Base
import library_modelo # Importa todos los modelos (libro, editora, etc.)

# Crea una instancia de FastAPI
app = FastAPI(title="Libreria API")

# --- Evento de Inicio: Crear la Base de Datos ---
# @app.on_event("startup") es una forma clásica de ejecutar código al inicio.
# Para FastAPI 0.100.0+ se prefiere @app.on_event("startup") o context managers (lifespan)
# Usaremos una función para ejecutar la creación de tablas.

# Función para crear las tablas
def create_db_tables():
    print("Creando todas las tablas en la base de datos...")
    # Base.metadata.create_all le dice a SQLAlchemy que use todos 
    # los modelos (clases que heredan de Base) importados para 
    # generar las tablas en el motor (engine) especificado.
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

# Llama a la función al iniciar la aplicación (antes de que maneje las peticiones)
create_db_tables()
# NOTA: En una aplicación de producción, la creación/migración de tablas
# se maneja mejor con herramientas como Alembic, pero para pruebas es suficiente.

# --- Rutas de Prueba (Opcional) ---
@app.get("/")
def read_root():
    return {"message": "API de Librería está funcionando"}