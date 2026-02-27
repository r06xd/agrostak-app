from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.shared.db import get_session
from app.identity.api.permissions import require_permissions
from app.reports.infra.repository import ReportsRepository
from app.reports.domain.schemas import DashboardSummary
from app.identity.api.deps import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/dashboard", response_model=DashboardSummary, dependencies=[Depends(require_permissions(["REPORTES_VER"]))])
def dashboard(db: Session = Depends(get_session)):
    repo = ReportsRepository(db)
    return repo.dashboard_summary()