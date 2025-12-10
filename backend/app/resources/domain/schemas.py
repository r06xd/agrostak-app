from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .entities import TipoRecurso, EstadoRecurso


class RecursoBase(BaseModel):
    nombre: str = Field(..., max_length=120)
    descripcion: Optional[str] = Field(None, max_length=255)
    tipo: TipoRecurso
    unidad_medida: str = Field(..., max_length=20)
    cantidad_disponible: Decimal = Field(default=0)
    ubicacion: Optional[str] = Field(None, max_length=100)
    estado: EstadoRecurso = EstadoRecurso.operativo


class RecursoCreate(RecursoBase):
    pass


class RecursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=120)
    descripcion: Optional[str] = Field(None, max_length=255)
    tipo: Optional[TipoRecurso] = None
    unidad_medida: Optional[str] = Field(None, max_length=20)
    cantidad_disponible: Optional[Decimal] = None
    ubicacion: Optional[str] = Field(None, max_length=100)
    estado: Optional[EstadoRecurso] = None


class RecursoRead(RecursoBase):
    id_recurso: int

    model_config = ConfigDict(from_attributes=True)
