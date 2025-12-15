"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""

from app.routers.api import carrito,genero,libro,usuario

from fastapi import APIRouter

# router principal
router = APIRouter()

# incluir router de songs en router principal
router.include_router(carrito.router)
router.include_router(genero.router)
router.include_router(libro.router)
router.include_router(usuario.router)
