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
        g8 = Genre(name="Historia")
        
        # agregar las canciones
        default_genres = [g1, g2, g3, g4, g5, g6, g7,g8]
        db.add_all(default_genres)
        
        # El commit es obligatorio para que obtengan su id.
        db.commit()
        
        # Inserción de Libros
        # Inserción de 9 Libros
        b1 = Libro(title="Napoleon", price=15.50, description="Vida y batallas del emperador.", genre_id=g7.id)
        b2 = Libro(title="El Resplandor", price=18.00, description="Pánico en el hotel Overlook.", genre_id=g1.id)
        b3 = Libro(title="La Isla del Tesoro", price=12.99, description="Piratas, mapas y tesoros escondidos.", genre_id=g5.id)
        b4 = Libro(title="Sapiens", price=22.40, description="Breve historia de la humanidad.", genre_id=g8.id)
        b5 = Libro(title="Don Quijote", price=25.00, description="El ingenioso hidalgo de la Mancha.", genre_id=g5.id)
        b6 = Libro(title="Robinson Crusoe", price=14.20, description="Naufragio y supervivencia en una isla.", genre_id=g6.id)
        b7 = Libro(title="Steve Jobs", price=19.95, description="La biografía oficial del genio de Apple.", genre_id=g7.id)
        b8 = Libro(title="Dracula", price=11.00, description="El clásico vampiro de Bram Stoker.", genre_id=g1.id)
        b9 = Libro(title="El Lazarillo de Tormes", price=10.50, description="Las andanzas de un joven pícaro.", genre_id=g5.id)
        
        default_libros = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
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
