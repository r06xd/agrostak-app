from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.shared.base_model import Base
from app.tasks.domain.enums import PrioridadTarea, EstadoTarea


class TareaORM(Base):
    __tablename__ = "tareas"

    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    id_tarea_padre = Column(Integer, ForeignKey("tareas.id_tarea"), nullable=True)
    id_creador = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    titulo = Column(String(150), nullable=False)
    descripcion = Column(String(255), nullable=True)

    fecha_creacion = Column(DateTime, nullable=False, server_default=func.now())
    fecha_inicio_prog = Column(DateTime, nullable=True)
    fecha_fin_prog = Column(DateTime, nullable=True)
    fecha_fin_real = Column(DateTime, nullable=True)

    prioridad = Column(Enum(PrioridadTarea), nullable=False, default=PrioridadTarea.media)
    estado = Column(Enum(EstadoTarea), nullable=False, default=EstadoTarea.pendiente)
    porcentaje_avance = Column(SmallInteger, nullable=False, default=0)
    es_recurrente = Column(SmallInteger, nullable=False, default=0)  # 0/1

    # Relaciones
    subtareas = relationship("TareaORM", remote_side=[id_tarea])
    asignaciones = relationship("AsignacionTareaORM", back_populates="tarea")
    historial = relationship("HistorialEstadoTareaORM", back_populates="tarea")
    comentarios = relationship("ComentarioTareaORM", back_populates="tarea")


class AsignacionTareaORM(Base):
    __tablename__ = "asignaciones_tarea"

    id_asignacion = Column(Integer, primary_key=True, autoincrement=True)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    fecha_asignacion = Column(DateTime, nullable=False, server_default=func.now())
    activo = Column(SmallInteger, nullable=False, default=1)

    tarea = relationship("TareaORM", back_populates="asignaciones")


class HistorialEstadoTareaORM(Base):
    __tablename__ = "historial_estados_tarea"

    id_historial = Column(Integer, primary_key=True, autoincrement=True)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"), nullable=False)
    estado_anterior = Column(Enum(EstadoTarea), nullable=True)
    estado_nuevo = Column(Enum(EstadoTarea), nullable=False)

    fecha_cambio = Column(DateTime, nullable=False, server_default=func.now())
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    comentario = Column(String(255), nullable=True)

    tarea = relationship("TareaORM", back_populates="historial")


class ComentarioTareaORM(Base):
    __tablename__ = "comentarios_tarea"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    texto = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False, server_default=func.now())

    tarea = relationship("TareaORM", back_populates="comentarios")
