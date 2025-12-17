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
from app.models.carrito import Carrito
from app.models.usuario import Usuario

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
def carrito(request: Request, db: Session = Depends(get_db)):
    # obtener items del carrito y transformar a estructuras simples para evitar cargas perezosas
    items = db.query(Carrito).all()
    items_data = []
    for it in items:
        libro = it.libro
        items_data.append({
            "id": it.id,
            "libro_id": libro.id if libro else None,
            "title": libro.title if libro else "(desconocido)",
            "price": float(libro.price) if libro and libro.price is not None else 0.0
        })
    return templates.TemplateResponse(
        "carrito.html",
        {"request": request, "items": items_data}
    )


@router.post("/carrito/add/{book_id}")
def carrito_add(book_id: int, db: Session = Depends(get_db)):
    # usar primer usuario por defecto (no hay autenticación en esta app)
    user = db.query(Usuario).first()
    if not user:
        return RedirectResponse(url="/", status_code=303)
    # confirmar que el libro existe
    libro = db.query(Libro).filter(Libro.id == book_id).first()
    if not libro:
        return RedirectResponse(url="/", status_code=303)
    # crear item de carrito
    item = Carrito(usuario_id=user.id, libro_id=book_id)
    db.add(item)
    db.commit()
    return RedirectResponse(url="/carrito", status_code=303)


@router.post("/carrito/delete/{item_id}")
def carrito_delete(item_id: int, db: Session = Depends(get_db)):
    it = db.query(Carrito).filter(Carrito.id == item_id).first()
    if it:
        db.delete(it)
        db.commit()
    return RedirectResponse(url="/carrito", status_code=303)


@router.post("/carrito/checkout")
def carrito_checkout(request: Request, db: Session = Depends(get_db)):
    # eliminar todos los items del carrito (compra completa)
    db.query(Carrito).delete()
    db.commit()
    # renderizar carrito con mensaje de compra realizada
    return templates.TemplateResponse(
        "carrito.html",
        {"request": request, "items": [], "bought": True}
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
def admin_generos(request: Request, db: Session = Depends(get_db)):
    # listar géneros
    generos = db.query(Genre).all()
    return templates.TemplateResponse(
        "generos.html",
        {"request": request, "genres": generos}
    )


@router.post("/generos/create")
def crear_genero(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    nombre = name.strip()
    if not nombre:
        return RedirectResponse(url="/generos", status_code=303)
    existing = db.query(Genre).filter(Genre.name == nombre).first()
    if existing:
        return RedirectResponse(url="/generos", status_code=303)
    g = Genre(name=nombre)
    db.add(g)
    db.commit()
    return RedirectResponse(url="/generos", status_code=303)


@router.post("/generos/delete/{genre_id}")
def borrar_genero(genre_id: int, db: Session = Depends(get_db)):
    g = db.query(Genre).filter(Genre.id == genre_id).first()
    if g:
        db.delete(g)
        db.commit()
    return RedirectResponse(url="/generos", status_code=303)


@router.get("/generos/edit/{genre_id}", response_class=HTMLResponse)
def editar_genero_get(request: Request, genre_id: int, db: Session = Depends(get_db)):
    g = db.query(Genre).filter(Genre.id == genre_id).first()
    return templates.TemplateResponse("generos_edit.html", {"request": request, "genre": g})


@router.post("/generos/edit/{genre_id}")
def editar_genero_post(request: Request, genre_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    g = db.query(Genre).filter(Genre.id == genre_id).first()
    if g:
        newname = name.strip()
        if newname:
            g.name = newname
            db.add(g)
            db.commit()
    return RedirectResponse(url="/generos", status_code=303)