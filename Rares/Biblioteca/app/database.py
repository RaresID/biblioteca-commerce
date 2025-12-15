"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.base import Base
from app.models import Genre, Libro, Usuario, Carrito



# crear motor de conexión a base de datos
engine = create_engine(
    "sqlite:///libreria.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()


# INICIALIZACIÓN BASE DE DATOS

# método inicializar con canciones por defecto
def init_db():
    """
    Inicializa la base de datos con todos los datos de
    géneros, libros, un usuario y un carrito por defecto
    en el caso de que todas las tablas estén vacías.
    """
        
    # crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        genres_existentes = db.execute(select(Genre)).scalars().all()
        
        if genres_existentes:
            print("La BBDD ya tiene los datos predeterminados. Su inicialización será realizada.")
            return
        
        print("--- Inicializando BBDD con los datos de la librería ---")
        
        # Inserción de Géneros
        g1 = Genre(name="Terror")        
        g2 = Genre(name="Comedia")       
        g3 = Genre(name="Accion")        
        g4 = Genre(name="Karate")        
        g5 = Genre(name="Aventura")      
        g6 = Genre(name="Supervivencia") 
        g7 = Genre(name="Biografia")
        
        # agregar las canciones
        default_genres = [g1, g2, g3, g4, g5, g6, g7]
        db.add_all(default_genres)
        
        # El commit es obligatorio para que obtengan su id.
        db.commit()
        
        # Inserción de Libros
        b1 = Libro(title="Napoleon", price=10.0, description="vacia1", genre_id=g7.id) # Biografia
        b2 = Libro(title="Misery", price=14.0, description="vacia2", genre_id=g1.id) # Terror
        b3 = Libro(title="La Boda de mi mejor amiga", price=19.99, description="vacia3", genre_id=g2.id) # Comedia
        b4 = Libro(title="guia de supervivencia", price=29.33, description="vacia4", genre_id=g6.id) # Supervivencia
        b5 = Libro(title="karate kid, el libro", price=29.33, description="vacia5", genre_id=g4.id) # Karate
        
        default_libros = [b1, b2, b3, b4, b5]
        db.add_all(default_libros)
        
        '''Inserciones únicas tanto usuario
        como carrito.'''
        u1 = Usuario(email="uno@example.com", password="secret1")
        db.add(u1)
        db.commit()
        
        c1 = Carrito(usuario_id=u1.id, libro_id=b1.id)
        db.add(c1)
        db.commit()
        
        print("--- La base de datos ha sido inicializada correctamente. ---")
    finally:
        db.close()
