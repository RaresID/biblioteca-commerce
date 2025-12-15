'''
Endpoints para carrito
'''

from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.models.carrito import Carrito
from app.schemas.carrito import CarritoResponse, CarritoCreate, CarritoFull
from app.database import get_db

router = APIRouter(
    prefix="/carrito",
    tags=["Carrito de Compras"]
)

def obtener_usuario_id() -> int:
    CURRENT_USER_ID = 1
    return CURRENT_USER_ID

CurrentUserID = Annotated[int, Depends(obtener_usuario_id)]

# 1. Obtener lista carrito
@router.get(
    "/ver_carrito",
    response_model=List[CarritoFull],
    summary="Ver todos los libros en el carrito del usuario actual"
)

def get_usuario_carro(user_id: CurrentUserID, db: Session = Depends(get_db)):
    '''Muestra de todos los elementos
    del carrito asociados con el usuario
    autenticado'''
    
    # Filtrado por id del usuario recogido en la dependencia
    items_carrito = db.query(Carrito).filter(Carrito.usuario_id == user_id).all()
    
    if not items_carrito:
        return []
    
    return items_carrito

# 2. Asignación del libro al carrito
@router.post(
    "/asignar_libro",
    response_model=CarritoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Asignación de un libro al carrito del usuario actual."
)

def asignar_libro_carro(libro_datos: CarritoCreate, user_id: CurrentUserID, db: Session = Depends(get_db)):
    '''Asigna un libro al carrito del usuario
    para asegurar que el id del usuario coincida
    con el autenticado.'''
    
    if libro_datos.usuario_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar el carro de otro usuario."
        )
    
    item_existente = db.query(Carrito).filter(
        Carrito.usuario_id == user_id,
        Carrito.libro_id == libro_datos.libro_id
    ).first()
    
    if item_existente:
        '''Como en carrito no hay campo cantidad,
        se asumirá su existencia con operación conflictiva
        de estado HTTP 409'''
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este libro ya está en el carro."
        )
    
    db_carrito_item = Carrito(
        usuario_id = user_id,
        libro_id = libro_datos.libro_id
    )
    
    try:
        db.add(db_carrito_item)
        db.commit()
        db.refresh(db_carrito_item)
        return db_carrito_item
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fallo en los datos. Aseguráte que el ID del libro sea válido."
        )

'''3. Borrado del carrito con DELET
y

4. Y para hacer la compra'''

@router.delete(
    "/eliminar_libro/{libro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Borrado de un libro específico del carro."
)

def borrar_libro_desde_carro(libro_id: int, user_id: CurrentUserID, db: Session = Depends(get_db)):
    '''Borrado del ítem exacto del carrito
    que pertenece al usuario y al libro.'''
    
    db_carrito_item = db.query(Carrito).filter(
        Carrito.usuario_id == user_id,
        Carrito.libro_id == libro_id
    ).first()
    
    if db_carrito_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con el ID {libro_id} no se encontró en tu carrito."
        )
    
    db.delete(db_carrito_item)
    db.commit()
    return

@router.delete(
    "/comprar_carrrito",
    status_code=status.HTTP_200_OK,
    summary="Al terminar la compra: borra todos los ítems del carrito y confirma el pedido"
)

def comprobacion_carro(user_id: CurrentUserID, db: Session = Depends(get_db)):
    '''Simulación de la compra mediante el borrado
    de todos los ítems del carro del usuario autenticado.'''
    
    items_a_borrar = db.query(Carrito).filter(Carrito.usuario_id == user_id).all()
    
    if not items_a_borrar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tu carro ya está vacío. No hay nada que comprar."
        )
    
    for item in items_a_borrar:
        db.delete(item)
    
    db.commit()
    
    return {"message": "¡Los libros han sido comprados con éxito! El carrito se está vaciando."}