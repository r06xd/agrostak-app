from typing import List, Optional
from sqlalchemy.orm import Session
from app.resources.infra.models import RecursoORM, RecursoTareaORM
from app.resources.domain.schemas import RecursoCreate, RecursoUpdate
from datetime import date
from sqlalchemy import func


class RecursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> List[RecursoORM]:
        return self.db.query(RecursoORM).all()

    def obtener(self, id_recurso: int) -> Optional[RecursoORM]:
        return self.db.query(RecursoORM).filter(RecursoORM.id_recurso == id_recurso).first()

    def crear(self, data: RecursoCreate) -> RecursoORM:
        recurso = RecursoORM(**data.dict())
        self.db.add(recurso)
        self.db.commit()
        self.db.refresh(recurso)
        return recurso

    def actualizar(self, id_recurso: int, data: RecursoUpdate) -> Optional[RecursoORM]:
        recurso = self.obtener(id_recurso)
        if not recurso:
            return None

        for field, value in data.dict(exclude_unset=True).items():
            setattr(recurso, field, value)

        self.db.commit()
        self.db.refresh(recurso)
        return recurso

    def eliminar(self, id_recurso: int) -> bool:
        recurso = self.obtener(id_recurso)
        if not recurso:
            return False
        self.db.delete(recurso)
        self.db.commit()
        return True

    def asignarRecursoTarea(self, id_recurso: int, id_tarea: int) -> bool:
        recursoTarea = RecursoTareaORM(id_recurso=id_recurso, id_tarea=id_tarea)
        self.db.add(recursoTarea)
        self.db.commit()
        return True
    
    def listar_insumos_por_acabarse(self, limite: int = 20) -> List[RecursoORM]:
        return (
            self.db.query(RecursoORM)
            .filter(
                RecursoORM.tipo == "insumo",
                RecursoORM.cantidad_disponible < limite
            )
            .order_by(RecursoORM.cantidad_disponible.asc(), RecursoORM.nombre.asc())
            .all()
        )

    def listar_herramientas_reparadas_hoy(self) -> List[RecursoORM]:
        hoy = date.today()

        return (
            self.db.query(RecursoORM)
            .filter(
                RecursoORM.tipo == "herramienta",
                RecursoORM.estado == "operativo",
                func.date(RecursoORM.fecha_reparacion) == hoy
            )
            .order_by(RecursoORM.fecha_reparacion.desc(), RecursoORM.nombre.asc())
            .all()
        )