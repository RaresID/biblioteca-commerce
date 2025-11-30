from pydantic import BaseModel, ConfigDict

class LibroBase(BaseModel):
    title: str
    price: int
    editor_id: int
    genre_id: int
    avaible: bool


class LibroCreate(LibroBase):
    pass


class LibroUpdate(BaseModel):
    title: str | None = None
    price: int | None = None
    editor_id: int | None = None
    genre_id: int | None = None
    avaible: bool | None = None


class LibroRead(LibroBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
class GenreBase(BaseModel):
    name: str
    
class GenreCreate(GenreBase):
    pass

class GenreUpdate(BaseModel):
    name: str | None = None

class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)    
