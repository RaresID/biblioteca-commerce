"""
Ruta web para página de inicio
Renderiza un HTML
"""

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.libro import Libro
from app.models.genero import Genre

# configurar jinja2
# usar la carpeta de plantillas (no el archivo) y ruta relativa al paquete
templates = Jinja2Templates(directory="app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    # obtener lista de libros desde la BBDD
    libros = db.query(Libro).all()
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "books": libros}
    )


@router.get("/carrito", response_class=HTMLResponse)
def carrito(request: Request):
    return templates.TemplateResponse(
        "carrito.html",
        {"request": request}
    )


@router.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    )


@router.get("/libros", response_class=HTMLResponse)
def admin_libros(request: Request, db: Session = Depends(get_db)):
    # obtener libros y géneros para listado y formularios
    libros = db.query(Libro).all()
    generos = db.query(Genre).all()
    return templates.TemplateResponse(
        "libros.html",
        {"request": request, "books": libros, "genres": generos}
    )


@router.post("/libros/create")
def crear_libro(request: Request,
                title: str = Form(...),
                price: float = Form(...),
                description: str = Form(...),
                genre_id: Optional[int] = Form(None),
                genre_name: Optional[str] = Form(None),
                db: Session = Depends(get_db)):
    # resolver género: usar genre_id si llega, sino crear/buscar por nombre
    if genre_id:
        gid = genre_id
    elif genre_name and genre_name.strip():
        name = genre_name.strip()
        existing = db.query(Genre).filter(Genre.name == name).first()
        if existing:
            gid = existing.id
        else:
            newg = Genre(name=name)
            db.add(newg)
            db.commit()
            db.refresh(newg)
            gid = newg.id
    else:
        # fallback: usar primer género disponible
        first = db.query(Genre).first()
        gid = first.id if first else None

    nuevo = Libro(title=title, price=price, description=description, genre_id=gid)
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/libros", status_code=303)


@router.post("/libros/delete/{libro_id}")
def borrar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro:
        db.delete(libro)
        db.commit()
    return RedirectResponse(url="/libros", status_code=303)


@router.get("/libros/edit/{libro_id}", response_class=HTMLResponse)
def editar_libro_get(request: Request, libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    generos = db.query(Genre).all()
    return templates.TemplateResponse("libros_edit.html", {"request": request, "book": libro, "genres": generos})


@router.post("/libros/edit/{libro_id}")
def editar_libro_post(request: Request,
                      libro_id: int,
                      title: str = Form(...),
                      price: float = Form(...),
                      description: str = Form(...),
                      genre_id: Optional[int] = Form(None),
                      genre_name: Optional[str] = Form(None),
                      db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if libro:
        # resolver género similar a crear
        if genre_id:
            gid = genre_id
        elif genre_name and genre_name.strip():
            name = genre_name.strip()
            existing = db.query(Genre).filter(Genre.name == name).first()
            if existing:
                gid = existing.id
            else:
                newg = Genre(name=name)
                db.add(newg)
                db.commit()
                db.refresh(newg)
                gid = newg.id
        else:
            gid = libro.genre_id

        libro.title = title
        libro.price = price
        libro.description = description
        libro.genre_id = gid
        db.add(libro)
        db.commit()
    return RedirectResponse(url="/libros", status_code=303)


@router.get("/generos", response_class=HTMLResponse)
def admin_generos(request: Request):
    return templates.TemplateResponse(
        "generos.html",
        {"request": request}
    )