from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.shared.db import get_session
from app.identity.domain.schemas import (
    LoginRequest, TokenResponse,
    UsuarioCreate, UsuarioUpdate, UsuarioRead
)
from app.identity.domain import services
from app.identity.api.deps import get_current_user
from app.identity.domain.schemas import PermisoRead, MenuItemRead

router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_session)):
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return services.login(db, data, ip, user_agent)


@router.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.list_users(db)


@router.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.create_user(db, data)


@router.put("/usuarios/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(id_usuario: int, data: UsuarioUpdate, db: Session = Depends(get_session), _=Depends(get_current_user)):
    return services.update_user(db, id_usuario, data)


@router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_session), _=Depends(get_current_user)):
    services.delete_user(db, id_usuario)
    return None


@router.get("/me", response_model=UsuarioRead)
def me(user=Depends(get_current_user)):
    return UsuarioRead.model_validate(user)

@router.post("/bootstrap/admin", response_model=UsuarioRead)
def bootstrap_admin(data: UsuarioCreate, db: Session = Depends(get_session)):
    return services.create_user(db, data)

@router.get("/permisos", response_model=list[PermisoRead])
def my_permissions(db=Depends(get_session), user=Depends(get_current_user)):
    return services.obtener_permisos_usuario(db, user)

@router.get("/menu", response_model=list[MenuItemRead])
def my_menu(db=Depends(get_session), user=Depends(get_current_user)):
    return services.obtener_menu_usuario(db, user)