from pydantic import BaseModel

class DashboardSummary(BaseModel):
    tareas_total: int
    tareas_pendientes: int
    tareas_en_progreso: int
    tareas_completadas: int
    tareas_canceladas: int
    tareas_vencidas: int

    recursos_total: int
    recursos_sin_stock: int
    recursos_en_mantenimiento: int