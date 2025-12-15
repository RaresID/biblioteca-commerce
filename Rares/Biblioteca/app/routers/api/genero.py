'''
Endpoints para genero
'''

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.models.genero import Genre
from app.schemas.genero import GenreRead, GenreCreate, GenreUpdate
from app.database import get_db

router = APIRouter(
    prefix="/genero",
    tags=["Géneros"],
)

# 1. Muestra completa de los géneros
@router.get(
    "/ver_generos",
    response_model=List[GenreRead],
    summary="Listado de todos los géneros"
)

def get_todos_generos(db: Session = Depends(get_db)):
    generos = db.query(Genre).all()
    return generos

# 2. Creación de género nuevo
@router.post(
    "/crear_genero",
    response_model=GenreRead,
    status_code=status.HTTP_201_CREATED,
    summary="Creación de género nuevo"
)

def crear_nuevo_genero(genero: GenreCreate, db: Session = Depends(get_db)):
    '''Para crear un nuevo género
    es obligatorio rellenar el campo nombre'''
    
    db_genero = Genre(**genero.model_dump())
    
    try:
        db.add(db_genero)
        db.commit()
        db.refresh(db_genero)
        return db_genero
    except exc.IntegrityError:
        db.rollback()
        
        '''La excepción del género captura errores
        para evitar nombres duplicados.'''
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fallo de integridad. El nombre de este género ya existe."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo inesperado al crear un género: {e}"
        )

# 3. Borrado de género por ID
@router.delete(
    "/borrar_genero/{genero_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Borrado de un género por ID."
)

def borrado_genero_id(genero_id: int, db: Session = Depends(get_db)):
    '''
    Se establecerá el borrado del género por su ID.
    
    Si el género está vinculado a libros, la base de datos
    evitará su borrado.
    '''
    db_genero = db.query(Genre).filter(Genre.id == genero_id).first()
    
    if db_genero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El género con ID {genero_id} es inexistente."
        )
    
    try:
        db.delete(db_genero)
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Borrado fallido. Todavía tienes libros vinculados a este género."
        )
    return

# 4. Actualización del género
@router.put(
    "/actualizar_genero/{genero_id}",
    response_model=GenreRead,
    summary="Cambio de nombre."
)

def update_genero_nombre(genero_id: int, genero_datos: GenreUpdate, db: Session = Depends(get_db)):
    db_genero = db.query(Genre).filter(Genre.id == genero_id).first()
    
    if db_genero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El género con ID {genero_id} no existe."
        )
    
    try:
        db_genero.name = genero_datos.name
        
        db.add(db_genero)
        db.commit()
        db.refresh(db_genero)
        return db_genero
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fallo de integridad. El nombre del género está en uso."
        )