"""
Ruta web para página de inicio
Renderiza un HTML
"""

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# configurar jinja2
# usar la carpeta de plantillas (no el archivo) y ruta relativa al paquete
templates = Jinja2Templates(directory="app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )