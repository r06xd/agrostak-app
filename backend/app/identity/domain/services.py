from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.identity.domain.schemas import (
    UsuarioCreate, UsuarioUpdate, UsuarioRead,
    LoginRequest, TokenResponse, RolRead
)
from app.identity.domain.validators import validate_password_strength
from app.identity.infra.repository import IdentityRepository
from app.identity.infra.models import UsuarioORM
from app.identity.infra.security import hash_password, verify_password, create_access_token
from app.config import settings
from app.identity.domain.schemas import PermisoRead, MenuItemRead


def create_user(db: Session, data: UsuarioCreate) -> UsuarioRead:
    repo = IdentityRepository(db)

    if repo.get_role(data.id_rol) is None:
        raise HTTPException(status_code=400, detail="El rol indicado no existe.")

    if repo.get_user_by_email(str(data.correo)) is not None:
        raise HTTPException(status_code=409, detail="El correo ya está registrado.")
    
    validate_base64_image(data.foto_url)

    validate_password_strength(data.password)

    user = UsuarioORM(
        id_rol=data.id_rol,
        nombres=data.nombres.strip(),
        apellidos=data.apellidos.strip(),
        correo=str(data.correo).lower().strip(),
        password_hash=hash_password(data.password),
        area_trabajo=data.area_trabajo,
        foto_url=data.foto_url,
        estado="activo",
    )

    created = repo.create_user(user)
    return UsuarioRead.model_validate(created)

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import base64

from app.identity.domain.schemas import (
    UsuarioCreate, UsuarioUpdate, UsuarioRead, LoginRequest, TokenResponse, RolRead
)
from app.identity.domain.validators import validate_password_strength
from app.identity.infra.repository import IdentityRepository
from app.identity.infra.models import UsuarioORM
from app.identity.infra.security import hash_password, verify_password, create_access_token
from app.config import settings
from app.identity.domain.schemas import PermisoRead, MenuItemRead


def validate_base64_image(foto_base64: str | None):
    if not foto_base64:
        return

    if not isinstance(foto_base64, str):
        raise HTTPException(status_code=400, detail="La imagen es inválida.")

    if not foto_base64.startswith("data:image/"):
        raise HTTPException(status_code=400, detail="La imagen debe venir en formato base64 válido.")

    if ";base64," not in foto_base64:
        raise HTTPException(status_code=400, detail="La imagen base64 es inválida.")

    try:
        header, encoded = foto_base64.split(";base64,", 1)
        base64.b64decode(encoded, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="La imagen base64 no pudo ser procesada.")


def update_user(db: Session, id_usuario: int, data: UsuarioUpdate) -> UsuarioRead:
    repo = IdentityRepository(db)
    user = repo.get_user_by_id(id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    print(data.foto_url)
    validate_base64_image(data.foto_url)

    payload = data.model_dump(exclude_unset=True)

    if "id_rol" in payload and repo.get_role(payload["id_rol"]) is None:
        raise HTTPException(status_code=400, detail="El rol indicado no existe.")

    if "correo" in payload:
        correo = str(payload["correo"]).lower().strip()
        other = repo.get_user_by_email(correo)
        if other and other.id_usuario != id_usuario:
            raise HTTPException(status_code=409, detail="El correo ya está registrado.")
        user.correo = correo

    if "password" in payload:
        try:
            validate_password_strength(payload["password"])
            user.password_hash = hash_password(payload["password"])
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    for field in ["id_rol", "nombres", "apellidos", "area_trabajo", "foto_url", "estado"]:
        if field in payload and field != "password":
            setattr(user, field, payload[field])
    updated = repo.update_user(user)
    return UsuarioRead.model_validate(updated)


def delete_user(db: Session, id_usuario: int) -> None:
    repo = IdentityRepository(db)
    user = repo.get_user_by_id(id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    repo.delete_user(user)

def listar_roles(db: Session) -> list[RolRead]:
    repo = IdentityRepository(db)
    return [RolRead.model_validate(r) for r in repo.list_roles()]


def list_users(db: Session) -> list[UsuarioRead]:
    repo = IdentityRepository(db)
    return [UsuarioRead.model_validate(u) for u in repo.list_users()]


def login(db: Session, data: LoginRequest, ip: str | None, user_agent: str | None) -> TokenResponse:
    repo = IdentityRepository(db)
    user = repo.get_user_by_email(str(data.correo).lower().strip())

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas.")

    if user.estado != "activo":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo.")

    # Actualiza último acceso + registra historial
    user.ultimo_acceso = datetime.utcnow()
    repo.update_user(user)
    repo.log_access(user.id_usuario, ip, user_agent)
    rol_str = repo.get_role(user.id_rol).nombre

    token = create_access_token(
        data={"sub": str(user.id_usuario), "role": str(user.id_rol), "rol": rol_str},
        secret_key=getattr(settings, "JWT_SECRET", "dev_secret_change_me"),
        expires_minutes=getattr(settings, "JWT_EXPIRES_MIN", 120),
    )
    return TokenResponse(access_token=token)

def obtener_permisos_usuario(db, user) -> list[PermisoRead]:
    repo = IdentityRepository(db)
    permisos = repo.get_role_permissions(user.id_rol)
    return [PermisoRead.model_validate(p) for p in permisos]

def obtener_menu_usuario(db, user) -> list[MenuItemRead]:
    repo = IdentityRepository(db)
    permisos = repo.get_role_permissions(user.id_rol)
    claves = set([p.clave for p in permisos])

    items = repo.list_menu_items()

    visibles = []
    for it in items:
        if it.permiso_clave is None:
            visibles.append(it)
        elif it.permiso_clave in claves:
            visibles.append(it)

    return [MenuItemRead.model_validate(x) for x in visibles]

def obtener_usuario_por_id(db, id_usuario):
    repo = IdentityRepository(db)
    return repo.get_user_by_id(id_usuario)

def obtener_usuario_admin(db):
    repo = IdentityRepository(db)
    return repo.get_user_admin()