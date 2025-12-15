'''
Endpoints para libro
'''

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.models.libro import Libro
from app.schemas.libro import LibroRead, LibroCreate, LibroPatch
from app.database import get_db

router = APIRouter(
    prefix="/libro",
    tags=["Libros"],
)

# 1. Listado completo de libros
@router.get(
    "/ver_libros",
    response_model=List[LibroRead],
    summary="Obtención absoluta de los libros"
)

def get_todos_libro(db: Session = Depends(get_db)):
    libros = db.query(Libro).all()
    
    '''Si no hay libros, devolverá una
    lista vacía y el código 200 (éxito)'''
    return libros

# 2. Creación libro nuevo
@router.post(
    "/crear_libro",
    response_model=LibroRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un libro nuevo"
)

def crear_nuevo_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    '''
    Crea un registro nuevo de libro en la base de datos.
    Requiere título, precio, descripción y genre_id.
    '''
    db_libro = Libro(**libro.model_dump())
    
    try:
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro
    except exc.IntegrityError:
        '''Con esta excepción captura fallos como por ejemplo
        la asignación de un genre_id que no aparece en la tabla
        genre.'''
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fallo de integridad. Asegúrate de que el id de género sea válido."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo inesperado al crear el libro: {e}"
        )

# 3. Borrado de libro por ID
@router.delete(
    "/borrar_libro/{libro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Borrado por ID"
)

def borrado_libro_id(libro_id: int, db: Session = Depends(get_db)):
    '''
    Borra un libro a través de su ID.
    Devuelve un código 204 (No Content) si lo borra correctamente.
    '''
    db_libro = db.query(Libro).filter(Libro.id == libro_id).first()
    
    if db_libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con ID {libro_id} no ha sido encontrado."
        )
    
    db.delete(db_libro)
    db.commit()

# 4. Actualización completa del libro
@router.put(
    "/actualizado_libro/{libro_id}",
    response_model=LibroRead,
    summary="Actualiza todos los campos aplicados hacia un libro"
)

def update_absoluto(libro_id: int, libro_datos: LibroCreate, db: Session = Depends(get_db)):
    '''Sustitución absoluta de un libro existente
    por otro nuevo con PUT.
    
    Es obligatorio rellenar todos los campos
    del esquema LibroCreate.'''
    
    db_libro = db.query(Libro).filter(Libro.id == libro_id).first()
    
    if db_libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con el ID {libro_id} no existe."
        )
    
    try:
        for llave, valor in libro_datos.model_dump().items():
            setattr(db_libro, llave, valor)
        
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fallo de integridad. Asegúrate que el ID de género sea válido."
        )

# 5. Actualización parcial del libro
@router.patch(
    "/actualizado_parcial/{libro_id}",
    response_model=LibroRead,
    summary="Modificación parcial de los campos para el libro."
)

def parcial_libro(libro_id: int, libro_datos: LibroPatch, db: Session = Depends(get_db)):
    '''
    Actualiza solo los campos proporcionados a través
    del esquema LibroPatch, siendo todos los campos
    opcionales.
    '''
    db_libro = db.query(Libro).filter(Libro.id == libro_id).first()
    
    if db_libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con ID {libro_id} no está disponible."
        )
    
    '''Conversión de los datos de Pydantic a diccionario
    sin contar con los valores None.'''
    modificar_dato = libro_datos.model_dump(exclude_unset=True)
    
    if not modificar_dato:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha proporcionado algún campo para modificar."
        )
    
    try:
        # Actualiza solo los campos presentes en el diccionario
        for clave, valor in modificar_dato.items():
            setattr(db_libro, clave, valor)
        
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fallo de integridad. Asegúrate de que el ID de género sea válido."
        )