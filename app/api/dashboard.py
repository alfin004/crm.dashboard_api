from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.services.dashboard_service import dashboard_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/staff-performance")
def get_staff_performance(
    sort_by: Literal["customer", "follow_up"] = "customer",
    db: Session = Depends(get_db),
):
    """List USER-role staff and their assigned customer/follow-up totals."""
    performance = dashboard_service.get_staff_performance(db, sort_by)
    return success_response(performance)
