from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.shared.db import get_session
from app.identity.api.permissions import require_permissions
from app.reports.infra.repository import ReportsRepository
from app.reports.domain.schemas import DashboardSummary
from app.identity.api.deps import get_current_user
from app.reports.domain.service import ReportsService

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/dashboard", response_model=DashboardSummary, dependencies=[Depends(require_permissions(["REPORTES_VER"]))])
def dashboard(db: Session = Depends(get_session)):
    repo = ReportsRepository(db)
    return repo.dashboard_summary()

@router.get("/dashboard/csv")
def export_dashboard_csv(db: Session = Depends(get_session)):
    repo = ReportsRepository(db)
    service = ReportsService(repo)

    csv_content = service.generate_dashboard_csv()

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=dashboard_report.csv"
        }
    )

@router.get("/dashboard/excel")
def export_dashboard_excel(db: Session = Depends(get_session)):
    repo = ReportsRepository(db)
    service = ReportsService(repo)

    excel_content = service.generate_dashboard_excel()

    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=dashboard_report.xlsx"
        }
    )