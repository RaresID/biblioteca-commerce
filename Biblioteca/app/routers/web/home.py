"""
Ruta web para página de inicio
Renderiza un HTML
"""


from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

# configurar jinja2
templates = Jinja2Templates(directory="app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=)