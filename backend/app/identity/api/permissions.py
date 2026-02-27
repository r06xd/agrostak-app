from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.shared.db import get_session
from app.identity.api.deps import get_current_user  # ajusta si tu archivo se llama distinto

def require_permissions(required: list[str]):
    def _dep(db: Session = Depends(get_session), user=Depends(get_current_user)):
        # Cargar permisos del rol (ya lo tienes con lazy="selectin")
        rol = user.rol  # debería estar disponible por la relationship
        if rol is None:
            raise HTTPException(status_code=403, detail="Usuario sin rol asignado")

        claves = {p.clave for p in rol.permisos}

        missing = [p for p in required if p not in claves]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes: {missing}"
            )
        return user

    return _dep