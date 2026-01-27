from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal


class RolRead(BaseModel):
    id_rol: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    id_rol: int = Field(..., gt=0)
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    area_trabajo: Optional[str] = Field(None, max_length=100)
    foto_url: Optional[str] = Field(None, max_length=255)


class UsuarioUpdate(BaseModel):
    id_rol: Optional[int] = Field(None, gt=0)
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=64)
    area_trabajo: Optional[str] = Field(None, max_length=100)
    foto_url: Optional[str] = Field(None, max_length=255)
    estado: Optional[Literal["activo", "inactivo"]] = None


class UsuarioRead(BaseModel):
    id_usuario: int
    id_rol: int
    nombres: str
    apellidos: str
    correo: EmailStr
    area_trabajo: Optional[str] = None
    foto_url: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PermisoRead(BaseModel):
    id_permiso: int
    clave: str
    descripcion: Optional[str] = None
    modulo: Optional[str] = None

    class Config:
        from_attributes = True

class MenuItemRead(BaseModel):
    clave: str
    label: str
    path: str
    icon: Optional[str] = None
    orden: int

    class Config:
        from_attributes = True