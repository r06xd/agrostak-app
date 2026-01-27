from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Table, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.shared.base_model import Base

class PermisoORM(Base):
    __tablename__ = "permisos"

    id_permiso = Column(Integer, primary_key=True, autoincrement=True)
    clave = Column(String(80), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    modulo = Column(String(50), nullable=True)

rol_permisos_table = Table(
    "rol_permisos",
    Base.metadata,
    Column("id_rol", Integer, ForeignKey("roles.id_rol", ondelete="CASCADE"), primary_key=True),
    Column("id_permiso", Integer, ForeignKey("permisos.id_permiso", ondelete="CASCADE"), primary_key=True),
)

class RolORM(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(200), nullable=True)

    usuarios = relationship("UsuarioORM", back_populates="rol")
    permisos = relationship("PermisoORM", secondary=rol_permisos_table, lazy="selectin")



class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)

    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    area_trabajo = Column(String(100), nullable=True)
    foto_url = Column(String(255), nullable=True)

    estado = Column(Enum("activo", "inactivo"), nullable=False, default="activo")
    fecha_creacion = Column(DateTime, nullable=False, server_default=func.now())
    ultimo_acceso = Column(DateTime, nullable=True)

    rol = relationship("RolORM", back_populates="usuarios")
    accesos = relationship("AccesoUsuarioORM", back_populates="usuario")


class AccesoUsuarioORM(Base):
    __tablename__ = "accesos_usuarios"
    id_acceso = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    fecha_login = Column(DateTime, nullable=False, server_default=func.now())
    ip = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)

    usuario = relationship("UsuarioORM", back_populates="accesos")

class MenuItemORM(Base):
    __tablename__ = "menu_items"

    id_menu = Column(Integer, primary_key=True, autoincrement=True)
    clave = Column(String(80), unique=True, nullable=False)
    label = Column(String(80), nullable=False)
    path = Column(String(120), nullable=False)
    icon = Column(String(40), nullable=True)
    orden = Column(Integer, nullable=False, default=1)
    permiso_clave = Column(String(80), nullable=True)
    activo = Column(Integer, nullable=False, default=1)