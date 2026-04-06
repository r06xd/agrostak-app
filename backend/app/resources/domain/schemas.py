from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .entities import TipoRecurso, EstadoRecurso
from datetime import datetime


class RecursoBase(BaseModel):
    nombre: str = Field(..., max_length=120)
    descripcion: Optional[str] = Field(None, max_length=255)
    tipo: TipoRecurso
    unidad_medida: str = Field(..., max_length=20)
    cantidad_disponible: Decimal = Field(default=0)
    ubicacion: Optional[str] = Field(None, max_length=100)
    estado: EstadoRecurso = EstadoRecurso.operativo
    cantidad_existente: Decimal = Field(default=0)


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
    cantidad_existente: Decimal = Field(default=0)


class RecursoRead(RecursoBase):
    id_recurso: int

    model_config = ConfigDict(from_attributes=True)

class RecursoAlertaItem(BaseModel):
    id_recurso: int
    nombre: str
    tipo: TipoRecurso
    cantidad_disponible: Decimal
    unidad_medida: str
    estado: EstadoRecurso
    ubicacion: Optional[str] = None
    fecha_reparacion: datetime

    model_config = ConfigDict(from_attributes=True)


class RecursoAlertasResumen(BaseModel):
    insumos_por_acabarse_total: int
    herramientas_reparadas_hoy_total: int
    insumos_por_acabarse: list[RecursoAlertaItem]
    herramientas_reparadas_hoy: list[RecursoAlertaItem]
