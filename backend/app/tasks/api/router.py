from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.tasks.domain.schemas import HistorialRead, CambiarEstadoRequest


from app.shared.db import get_session
from app.identity.api.deps import get_current_user
from app.tasks.domain.schemas import (
    TareaCreate, TareaUpdate, TareaRead,
    AsignacionCreate, AsignacionRead,
    ComentarioCreate, ComentarioRead,TareaListOut
)
from app.tasks.domain import services

router = APIRouter(prefix="/tareas", tags=["tareas"])


@router.get("/", response_model=list[TareaListOut])
def list_tareas(db: Session = Depends(get_session), user=Depends(get_current_user)):
    print('Entra a buscar tareas')
    if user.id_rol == 1:
        return services.listar_tareas(db)
    else:
        print('Entra a buscar por usuario', user.id_usuario)
        services.mis_tareas(db, id_usuario=user.id_usuario)


@router.post("/", response_model=TareaRead, status_code=status.HTTP_201_CREATED)
def create_tarea(data: TareaCreate, db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.crear_tarea(db, data, id_creador=user.id_usuario)


@router.get("/{id_tarea}", response_model=TareaRead)
def get_tarea(id_tarea: int, db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.obtener_tarea(db, id_tarea)


@router.put("/{id_tarea}", response_model=TareaRead)
def update_tarea(id_tarea: int, data: TareaUpdate, db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.actualizar_tarea(db, id_tarea, data, id_usuario=user.id_usuario)


@router.delete("/{id_tarea}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tarea(id_tarea: int, db: Session = Depends(get_session), _=Depends(get_current_user)):
    services.eliminar_tarea(db, id_tarea)
    return None


# Asignaciones
@router.post("/{id_tarea}/assign", response_model=AsignacionRead, status_code=status.HTTP_201_CREATED)
def assign_user(id_tarea: int, data: AsignacionCreate, db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.asignar_usuario(db, id_tarea, data, id_usuario_actor=user.id_usuario)

@router.post("/{id_tarea}/assignUser/{id_usuario}", response_model=AsignacionRead, status_code=status.HTTP_201_CREATED)
def assign_user(id_tarea: int, id_usuario: int, data: AsignacionCreate, db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.asignar_usuario(db, id_tarea, data, id_usuario_actor=user.id_usuario)


@router.get("/{id_tarea}/assign", response_model=list[AsignacionRead])
def list_assign(id_tarea: int, db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.listar_asignaciones(db, id_tarea)


# Comentarios
@router.post("/{id_tarea}/comments", response_model=ComentarioRead, status_code=status.HTTP_201_CREATED)
def add_comment(id_tarea: int, data: ComentarioCreate, db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.agregar_comentario(db, id_tarea, data, id_usuario=user.id_usuario)


@router.get("/{id_tarea}/comments", response_model=list[ComentarioRead])
def list_comments(id_tarea: int, db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.listar_comentarios(db, id_tarea)

@router.get("/my", response_model=list[TareaRead])
def my_tasks(db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.mis_tareas(db, id_usuario=user.id_usuario)

@router.get("/{id_tarea}/history", response_model=list[HistorialRead])
def task_history(id_tarea: int, db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.obtener_historial(db, id_tarea)

@router.post("/{id_tarea}/status", response_model=TareaRead)
def change_status(id_tarea: int, data: CambiarEstadoRequest, db: Session = Depends(get_session), user=Depends(get_current_user)):
    return services.cambiar_estado(db, id_tarea, data, id_usuario=user.id_usuario)
