from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.tasks.domain.enums import PrioridadTarea, EstadoTarea


class TareaCreate(BaseModel):
    id_tarea_padre: Optional[int] = None
    titulo: str = Field(..., min_length=3, max_length=150)
    descripcion: str = Field(..., min_length=3)
    fecha_inicio_prog: Optional[datetime] = None
    fecha_fin_prog: Optional[datetime] = None
    prioridad: PrioridadTarea = PrioridadTarea.media
    es_recurrente: bool = False


class TareaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=150)
    descripcion: Optional[str] = Field(None, min_length=3)
    fecha_inicio_prog: Optional[datetime] = None
    fecha_fin_prog: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    prioridad: Optional[PrioridadTarea] = None
    estado: Optional[EstadoTarea] = None
    porcentaje_avance: Optional[int] = Field(None, ge=0, le=100)
    es_recurrente: Optional[bool] = None

class TareaListOut(BaseModel):
    id_tarea: int
    titulo: str
    estado: str
    prioridad: str
    porcentaje_avance: int

    # los que te faltan: ponlos opcionales o inclúyelos
    fecha_creacion: Optional[datetime] = None
    fecha_inicio_prog: Optional[datetime] = None
    fecha_fin_prog: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    es_recurrente: Optional[bool] = None

    asignado_a: Optional[str] = None

class TareaRead(BaseModel):
    id_tarea: int
    id_tarea_padre: Optional[int]
    id_creador: int
    titulo: str
    descripcion: str
    fecha_creacion: datetime
    fecha_inicio_prog: Optional[datetime]
    fecha_fin_prog: Optional[datetime]
    fecha_fin_real: Optional[datetime]
    prioridad: PrioridadTarea
    estado: EstadoTarea
    porcentaje_avance: int
    es_recurrente: bool

    class Config:
        from_attributes = True


class AsignacionCreate(BaseModel):
    id_usuario: int = Field(..., gt=0)


class AsignacionRead(BaseModel):
    id_asignacion: int
    id_tarea: int
    id_usuario: int
    fecha_asignacion: datetime
    activo: int

    class Config:
        from_attributes = True


class ComentarioCreate(BaseModel):
    texto: str = Field(..., min_length=1)


class ComentarioRead(BaseModel):
    id_comentario: int
    id_tarea: int
    id_usuario: int
    texto: str
    fecha: datetime

    class Config:
        from_attributes = True

class HistorialRead(BaseModel):
    id_historial: int
    id_tarea: int
    estado_anterior: EstadoTarea | None
    estado_nuevo: EstadoTarea
    fecha_cambio: datetime
    id_usuario: int
    comentario: str | None = None

    class Config:
        from_attributes = True


class CambiarEstadoRequest(BaseModel):
    estado: EstadoTarea
    comentario: str | None = Field(default=None, max_length=255)
