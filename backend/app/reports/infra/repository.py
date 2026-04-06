from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime

from app.tasks.infra.models import TareaORM
from app.resources.infra.models import RecursoORM
from datetime import datetime
from sqlalchemy import and_

class ReportsRepository:
    def __init__(self, db: Session):
        self.db = db

    def dashboard_summary(self, fecha_inicio=None, fecha_fin=None):
        now = datetime.utcnow()

        # ---- FILTRO DINÁMICO ----
        filtros = []
        if fecha_inicio:
            filtros.append(func.date(TareaORM.fecha_creacion) >= fecha_inicio)

        if fecha_fin:
            filtros.append(func.date(TareaORM.fecha_creacion) <= fecha_fin)

        # ---- QUERY TAREAS ----
        query_tareas = self.db.query(
            func.count(TareaORM.id_tarea).label("total"),
            func.sum(case((TareaORM.estado == "pendiente", 1), else_=0)).label("pendientes"),
            func.sum(case((TareaORM.estado == "en_progreso", 1), else_=0)).label("en_progreso"),
            func.sum(case((TareaORM.estado == "completada", 1), else_=0)).label("completadas"),
            func.sum(case((TareaORM.estado == "cancelada", 1), else_=0)).label("canceladas"),
            func.sum(
                case((
                    (TareaORM.fecha_fin_prog.isnot(None)) &
                    (TareaORM.fecha_fin_prog < now) &
                    (TareaORM.estado != "completada"),
                    1
                ), else_=0)
            ).label("vencidas"),
        )

        # Aplicar filtros si existen
        if filtros:
            query_tareas = query_tareas.filter(and_(*filtros))

        print(str(query_tareas.statement.compile(compile_kwargs={"literal_binds": True})))
        tareas = query_tareas.one()

        # ---- RECURSOS (sin filtro por ahora) ----
        recursos = self.db.query(
            func.count(RecursoORM.id_recurso).label("total"),
            func.sum(case((RecursoORM.cantidad_disponible <= 0, 2), else_=0)).label("sin_stock"),
            func.sum(case((RecursoORM.estado == "mantenimiento", 1), else_=0)).label("mantenimiento"),
        ).one()

        return {
            "tareas_total": int(tareas.total or 0),
            "tareas_pendientes": int(tareas.pendientes or 0),
            "tareas_en_progreso": int(tareas.en_progreso or 0),
            "tareas_completadas": int(tareas.completadas or 0),
            "tareas_canceladas": int(tareas.canceladas or 0),
            "tareas_vencidas": int(tareas.vencidas or 0),

            "recursos_total": int(recursos.total or 0),
            "recursos_sin_stock": int(recursos.sin_stock or 0),
            "recursos_en_mantenimiento": int(recursos.mantenimiento or 0),
        }