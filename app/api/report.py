from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user, security
from app.dependencies.db import get_db
from app.core.response import success_response
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)


# ---------------- Customer report ----------------

@router.get("/customers")
async def get_customer_report(
        district: str = None,
        staff_id: UUID = None,
        status: str = None,
        is_active: bool = None,
        product_id: UUID = None,
        registration_date_from: date = None,
        registration_date_to: date = None,
        sort_by: str = "registered_on",
        sort_order: str = "desc",
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    result = await ReportService.customer_report(
        db=db,
        token=credentials.credentials,
        district=district,
        staff_id=staff_id,
        customer_status=status,
        is_active=is_active,
        product_id=product_id,
        registration_date_from=registration_date_from,
        registration_date_to=registration_date_to,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )

    return success_response(result)


@router.get("/customers/export")
async def export_customer_report(
        district: str = None,
        staff_id: UUID = None,
        status: str = None,
        is_active: bool = None,
        product_id: UUID = None,
        registration_date_from: date = None,
        registration_date_to: date = None,
        sort_by: str = "registered_on",
        sort_order: str = "desc",
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    return await ReportService.customer_report_export(
        db=db,
        token=credentials.credentials,
        district=district,
        staff_id=staff_id,
        customer_status=status,
        is_active=is_active,
        product_id=product_id,
        registration_date_from=registration_date_from,
        registration_date_to=registration_date_to,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ---------------- Product report ----------------

@router.get("/products")
async def get_product_report(
        product_id: UUID = None,
        purchase_date_from: date = None,
        purchase_date_to: date = None,
        sort_by: str = "product_name",
        sort_order: str = "asc",
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db)):

    result = ReportService.product_report(
        db=db,
        product_id=product_id,
        purchase_date_from=purchase_date_from,
        purchase_date_to=purchase_date_to,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )

    return success_response(result)


@router.get("/products/export")
async def export_product_report(
        product_id: UUID = None,
        purchase_date_from: date = None,
        purchase_date_to: date = None,
        sort_by: str = "product_name",
        sort_order: str = "asc",
        db: Session = Depends(get_db)):

    return ReportService.product_report_export(
        db=db,
        product_id=product_id,
        purchase_date_from=purchase_date_from,
        purchase_date_to=purchase_date_to,
        sort_by=sort_by,
        sort_order=sort_order
    )


# ---------------- Follow-up report ----------------

@router.get("/follow-ups")
async def get_follow_up_report(
        product_id: UUID = None,
        follow_up_status: str = None,
        staff_id: UUID = None,
        date_from: date = None,
        date_to: date = None,
        sort_by: str = "remarks_date",
        sort_order: str = "desc",
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    result = await ReportService.follow_up_report(
        db=db,
        token=credentials.credentials,
        product_id=product_id,
        follow_up_status=follow_up_status,
        staff_id=staff_id,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )

    return success_response(result)


@router.get("/follow-ups/export")
async def export_follow_up_report(
        product_id: UUID = None,
        follow_up_status: str = None,
        staff_id: UUID = None,
        date_from: date = None,
        date_to: date = None,
        sort_by: str = "remarks_date",
        sort_order: str = "desc",
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    return await ReportService.follow_up_report_export(
        db=db,
        token=credentials.credentials,
        product_id=product_id,
        follow_up_status=follow_up_status,
        staff_id=staff_id,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order
    )
