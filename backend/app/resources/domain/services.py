from sqlalchemy.orm import Session
from typing import List, Optional
from app.resources.infra.repository import RecursoRepository
from app.resources.domain.schemas import (
    RecursoCreate,
    RecursoUpdate,
    RecursoRead,
    RecursoAlertaItem,
    RecursoAlertasResumen,
)
from app.notifications.infra.onesignal_client import send_resource_status_push
from app.identity.infra.repository import IdentityRepository


def listar_recursos(db: Session) -> List[RecursoRead]:
    repo = RecursoRepository(db)
    recursos = repo.listar()
    return [RecursoRead.from_orm(r) for r in recursos]


def obtener_recurso(db: Session, id_recurso: int) -> Optional[RecursoRead]:
    repo = RecursoRepository(db)
    recurso = repo.obtener(id_recurso)
    if not recurso:
        return None
    return RecursoRead.from_orm(recurso)


def crear_recurso(db: Session, data: RecursoCreate) -> RecursoRead:
    repo = RecursoRepository(db)
    recurso = repo.crear(data)
    return RecursoRead.from_orm(recurso)


def actualizar_recurso(db: Session, id_recurso: int, data: RecursoUpdate) -> Optional[RecursoRead]:
    repo = RecursoRepository(db)
    recurso = repo.actualizar(id_recurso, data)
    if not recurso:
        return None
    return RecursoRead.from_orm(recurso)


def eliminar_recurso(db: Session, id_recurso: int) -> bool:
    repo = RecursoRepository(db)
    return repo.eliminar(id_recurso)

def asignarRecursoTarea(db: Session, id_recurso: int, id_tarea: int) -> bool:
    repo = RecursoRepository(db)
    return repo.asignarRecursoTarea(id_recurso, id_tarea)

def enviarNotificacion(db: Session,estado: str, id_recurso: int):
    repoIdentity = IdentityRepository(db)
    id_usuario = repoIdentity.get_user_admin(id_recurso);
    send_resource_status_push(id_usuario, estado, id_recurso)

def obtener_alertas_resumen(db: Session) -> RecursoAlertasResumen:
    repo = RecursoRepository(db)

    insumos = repo.listar_insumos_por_acabarse(20)
    herramientas = repo.listar_herramientas_reparadas_hoy()

    return RecursoAlertasResumen(
        insumos_por_acabarse_total=len(insumos),
        herramientas_reparadas_hoy_total=len(herramientas),
        insumos_por_acabarse=[RecursoAlertaItem.from_orm(r) for r in insumos],
        herramientas_reparadas_hoy=[RecursoAlertaItem.from_orm(r) for r in herramientas],
    )