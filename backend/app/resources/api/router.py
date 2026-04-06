from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.shared.db import get_session
from app.resources.domain.schemas import (
    RecursoCreate,
    RecursoUpdate,
    RecursoRead,
    RecursoAlertasResumen,
)
from app.resources.domain import services as recurso_service
from app.identity.api.deps import get_current_user

router = APIRouter(prefix="/recursos", tags=["recursos"])

@router.get("/prueba")
def prueba_api():
    return "Hola mundo"

@router.get("/", response_model=List[RecursoRead])
def listar_recursos(db: Session = Depends(get_session)):
    return recurso_service.listar_recursos(db)


@router.get("/{id_recurso}", response_model=RecursoRead)
def obtener_recurso(id_recurso: int, db: Session = Depends(get_session)):
    recurso = recurso_service.obtener_recurso(db, id_recurso)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado",
        )
    return recurso


@router.post("/", response_model=RecursoRead, status_code=status.HTTP_201_CREATED)
def crear_recurso(data: RecursoCreate, db: Session = Depends(get_session)):
    return recurso_service.crear_recurso(db, data)


@router.put("/{id_recurso}", response_model=RecursoRead)
def actualizar_recurso(
    id_recurso: int,
    data: RecursoUpdate,
    db: Session = Depends(get_session),
):
    recurso = recurso_service.actualizar_recurso(db, id_recurso, data)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado",
        )
    return recurso
    


@router.delete("/{id_recurso}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_recurso(id_recurso: int, db: Session = Depends(get_session)):
    ok = recurso_service.eliminar_recurso(db, id_recurso)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado",
        )
    return None

@router.post("/assignResource/{id_tarea}/{id_recurso}/{cantidad}", response_model=bool, status_code=status.HTTP_201_CREATED)
def asignarRecursoTarea(id_recurso: int, id_tarea: int, cantidad:int, db: Session = Depends(get_session)):
    return recurso_service.asignarRecursoTarea(db, id_recurso, id_tarea, cantidad)

@router.post("/sendNotification/{id_recurso}/{estado}", response_model=bool, status_code=status.HTTP_201_CREATED)
def asignarRecursoTarea(id_recurso: int, estado: str, db: Session = Depends(get_session)):
    return recurso_service.enviarNotificacion(db, estado, id_recurso)

@router.get("/alertas/resumen", response_model=RecursoAlertasResumen)
def obtener_alertas_resumen(db: Session = Depends(get_session)):
    return recurso_service.obtener_alertas_resumen(db)