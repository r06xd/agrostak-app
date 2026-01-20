from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.tasks.domain.schemas import HistorialRead, CambiarEstadoRequest
from app.tasks.infra.models import HistorialEstadoTareaORM

from app.tasks.domain.schemas import (
    TareaCreate, TareaUpdate, TareaRead,
    AsignacionCreate, AsignacionRead,
    ComentarioCreate, ComentarioRead
)
from app.tasks.infra.repository import TasksRepository
from app.tasks.infra.models import TareaORM, AsignacionTareaORM, HistorialEstadoTareaORM, ComentarioTareaORM
from app.tasks.domain.enums import EstadoTarea


def crear_tarea(db: Session, data: TareaCreate, id_creador: int) -> TareaRead:
    repo = TasksRepository(db)

    if data.id_tarea_padre:
        parent = repo.get_tarea(data.id_tarea_padre)
        if not parent:
            raise HTTPException(status_code=400, detail="La tarea padre no existe.")

    if data.fecha_inicio_prog and data.fecha_fin_prog and data.fecha_inicio_prog > data.fecha_fin_prog:
        raise HTTPException(status_code=400, detail="fecha_inicio_prog no puede ser mayor que fecha_fin_prog.")

    tarea = TareaORM(
        id_tarea_padre=data.id_tarea_padre,
        id_creador=id_creador,
        titulo=data.titulo.strip(),
        descripcion=data.descripcion.strip(),
        fecha_inicio_prog=data.fecha_inicio_prog,
        fecha_fin_prog=data.fecha_fin_prog,
        prioridad=data.prioridad,
        estado=EstadoTarea.pendiente,
        porcentaje_avance=0,
        es_recurrente=1 if data.es_recurrente else 0,
    )

    created = repo.create_tarea(tarea)

    # historial inicial
    repo.add_historial(HistorialEstadoTareaORM(
        id_tarea=created.id_tarea,
        estado_anterior=None,
        estado_nuevo=created.estado,
        id_usuario=id_creador,
        comentario="Creación de tarea"
    ))

    return TareaRead.model_validate(created)


def listar_tareas(db: Session) -> list[TareaRead]:
    repo = TasksRepository(db)
    return [TareaRead.model_validate(t) for t in repo.list_tareas()]


def obtener_tarea(db: Session, id_tarea: int) -> TareaRead:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    return TareaRead.model_validate(tarea)


def actualizar_tarea(db: Session, id_tarea: int, data: TareaUpdate, id_usuario: int) -> TareaRead:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")

    payload = data.model_dump(exclude_unset=True)

    if "fecha_inicio_prog" in payload and "fecha_fin_prog" in payload:
        if payload["fecha_inicio_prog"] and payload["fecha_fin_prog"] and payload["fecha_inicio_prog"] > payload["fecha_fin_prog"]:
            raise HTTPException(status_code=400, detail="fecha_inicio_prog no puede ser mayor que fecha_fin_prog.")

    estado_anterior = tarea.estado

    for field in ["titulo", "descripcion", "fecha_inicio_prog", "fecha_fin_prog", "fecha_fin_real", "prioridad", "estado", "porcentaje_avance"]:
        if field in payload and payload[field] is not None:
            setattr(tarea, field, payload[field] if field not in ["titulo","descripcion"] else str(payload[field]).strip())

    if "es_recurrente" in payload and payload["es_recurrente"] is not None:
        tarea.es_recurrente = 1 if payload["es_recurrente"] else 0

    # regla simple: si estado pasa a completada, avance 100 y fecha_fin_real si no existe
    if "estado" in payload and payload["estado"] == EstadoTarea.completada:
        tarea.porcentaje_avance = 100
        if not tarea.fecha_fin_real:
            tarea.fecha_fin_real = datetime.utcnow()

    updated = repo.update_tarea(tarea)

    # historial si cambió estado
    if "estado" in payload and payload["estado"] != estado_anterior:
        repo.add_historial(HistorialEstadoTareaORM(
            id_tarea=id_tarea,
            estado_anterior=estado_anterior,
            estado_nuevo=updated.estado,
            id_usuario=id_usuario,
            comentario="Cambio de estado"
        ))

    return TareaRead.model_validate(updated)


def eliminar_tarea(db: Session, id_tarea: int) -> None:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    repo.delete_tarea(tarea)


def asignar_usuario(db: Session, id_tarea: int, data: AsignacionCreate, id_usuario_actor: int) -> AsignacionRead:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")

    asignacion = AsignacionTareaORM(
        id_tarea=id_tarea,
        id_usuario=data.id_usuario,
        activo=1
    )
    created = repo.add_asignacion(asignacion)

    # historial (opcional)
    repo.add_historial(HistorialEstadoTareaORM(
        id_tarea=id_tarea,
        estado_anterior=tarea.estado,
        estado_nuevo=tarea.estado,
        id_usuario=id_usuario_actor,
        comentario=f"Asignación de usuario {data.id_usuario}"
    ))

    return AsignacionRead.model_validate(created)


def listar_asignaciones(db: Session, id_tarea: int) -> list[AsignacionRead]:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    return [AsignacionRead.model_validate(a) for a in repo.list_asignaciones(id_tarea)]


def agregar_comentario(db: Session, id_tarea: int, data: ComentarioCreate, id_usuario: int) -> ComentarioRead:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")

    comentario = ComentarioTareaORM(
        id_tarea=id_tarea,
        id_usuario=id_usuario,
        texto=data.texto.strip()
    )
    created = repo.add_comentario(comentario)
    return ComentarioRead.model_validate(created)


def listar_comentarios(db: Session, id_tarea: int) -> list[ComentarioRead]:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    return [ComentarioRead.model_validate(c) for c in repo.list_comentarios(id_tarea)]

def obtener_historial(db: Session, id_tarea: int) -> list[HistorialRead]:
    repo = TasksRepository(db)

    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")

    historial = repo.list_historial(id_tarea)
    return [HistorialRead.model_validate(h) for h in historial]

def mis_tareas(db: Session, id_usuario: int) -> list[TareaRead]:
    repo = TasksRepository(db)
    tareas = repo.list_tareas_by_assignee(id_usuario)
    return [TareaRead.model_validate(t) for t in tareas]

def cambiar_estado(db: Session, id_tarea: int, data: CambiarEstadoRequest, id_usuario: int) -> TareaRead:
    repo = TasksRepository(db)
    tarea = repo.get_tarea(id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")

    estado_anterior = tarea.estado
    tarea.estado = data.estado

    # reglas simples
    if data.estado == EstadoTarea.completada:
        tarea.porcentaje_avance = 100
        if not tarea.fecha_fin_real:
            tarea.fecha_fin_real = datetime.utcnow()

    updated = repo.update_tarea(tarea)

    repo.add_historial(
        HistorialEstadoTareaORM(
            id_tarea=id_tarea,
            estado_anterior=estado_anterior,
            estado_nuevo=updated.estado,
            id_usuario=id_usuario,
            comentario=data.comentario or "Cambio de estado"
        )
    )

    return TareaRead.model_validate(updated)
