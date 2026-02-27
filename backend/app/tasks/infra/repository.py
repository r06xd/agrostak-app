from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.tasks.infra.models import (
    TareaORM, AsignacionTareaORM, HistorialEstadoTareaORM, ComentarioTareaORM
)
from app.identity.infra.models import UsuarioORM

from app.tasks.domain.enums import EstadoTarea


class TasksRepository:
    def __init__(self, db: Session):
        self.db = db

    # ----- TAREAS -----
    def list_tareas(self) -> List[TareaORM]:
        return self.db.query(TareaORM).all()
    
    def list_tareas_con_asignado(self):
        return (
            self.db.query(
                TareaORM,
                UsuarioORM.nombres,
                UsuarioORM.apellidos
            )
            .outerjoin(
                AsignacionTareaORM,
                AsignacionTareaORM.id_tarea == TareaORM.id_tarea
            )
            .outerjoin(
                UsuarioORM,
                UsuarioORM.id_usuario == AsignacionTareaORM.id_usuario
            )
            .filter(
                (AsignacionTareaORM.activo == 1) | (AsignacionTareaORM.activo.is_(None))
            )
            .all()
        )   

    def get_tarea(self, id_tarea: int) -> Optional[TareaORM]:
        return self.db.query(TareaORM).filter(TareaORM.id_tarea == id_tarea).first()

    def create_tarea(self, tarea: TareaORM) -> TareaORM:
        self.db.add(tarea)
        self.db.commit()
        self.db.refresh(tarea)
        return tarea

    def update_tarea(self, tarea: TareaORM) -> TareaORM:
        self.db.commit()
        self.db.refresh(tarea)
        return tarea

    def delete_tarea(self, tarea: TareaORM) -> None:
        self.db.delete(tarea)
        self.db.commit()

    # ----- ASIGNACIONES -----
    def add_asignacion(self, asignacion: AsignacionTareaORM) -> AsignacionTareaORM:
        self.db.add(asignacion)
        self.db.commit()
        self.db.refresh(asignacion)
        return asignacion
    
    def update_asignacion(self, asignacion: AsignacionTareaORM) -> AsignacionTareaORM:
        self.db.commit()
        self.db.refresh(asignacion)
        return asignacion
    
    def delete_asignacion(self, asignacion: AsignacionTareaORM) -> None:
        self.db.delete(asignacion)
        self.db.commit()

    def list_asignaciones(self, id_tarea: int) -> List[AsignacionTareaORM]:
        return self.db.query(AsignacionTareaORM).filter(AsignacionTareaORM.id_tarea == id_tarea).all()

    # ----- HISTORIAL -----
    def add_historial(self, hist: HistorialEstadoTareaORM) -> None:
        self.db.add(hist)
        self.db.commit()

    # ----- COMENTARIOS -----
    def add_comentario(self, comentario: ComentarioTareaORM) -> ComentarioTareaORM:
        self.db.add(comentario)
        self.db.commit()
        self.db.refresh(comentario)
        return comentario

    def list_comentarios(self, id_tarea: int) -> List[ComentarioTareaORM]:
        return self.db.query(ComentarioTareaORM).filter(ComentarioTareaORM.id_tarea == id_tarea).all()

def list_historial(self, id_tarea: int):
    return (
        self.db.query(HistorialEstadoTareaORM)
        .filter(HistorialEstadoTareaORM.id_tarea == id_tarea)
        .order_by(desc(HistorialEstadoTareaORM.fecha_cambio))
        .all()
    )

def list_tareas_by_assignee(self, id_usuario: int):
    # Join asignaciones -> tareas
    return (
        self.db.query(TareaORM)
        .join(AsignacionTareaORM, AsignacionTareaORM.id_tarea == TareaORM.id_tarea)
        .filter(AsignacionTareaORM.id_usuario == id_usuario)
        .filter(AsignacionTareaORM.activo == 1)
        .all()
    )
