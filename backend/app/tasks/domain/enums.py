from enum import Enum

class PrioridadTarea(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"
    cancelada = "cancelada"
    eliminada = "eliminada"
