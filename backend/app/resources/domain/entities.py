from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class TipoRecurso(str, Enum):
    insumo = "insumo"
    herramienta = "herramienta"
    maquinaria = "maquinaria"
    otro = "otro"


class EstadoRecurso(str, Enum):
    operativo = "operativo"
    mantenimiento = "mantenimiento"
    inactivo = "inactivo"


@dataclass
class Recurso:
    id: int | None
    nombre: str
    descripcion: str | None
    tipo: TipoRecurso
    unidad_medida: str
    cantidad_disponible: Decimal
    ubicacion: str | None
    estado: EstadoRecurso
