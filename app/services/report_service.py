from datetime import date
from io import BytesIO
from uuid import UUID

from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.core.context import current_user_context
from app.repositories.report_repository import report_repository
from app.services.staff_service import staff_service


def _staff_name(directory: dict, staff_id):
    if not staff_id:
        return None
    return directory.get(staff_id) or directory.get(str(staff_id)) or str(staff_id)


def _format_date(value):
    return value.strftime("%Y-%m-%d") if value else ""


def _excel_response(headers, rows, filename):
    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    for row in rows:
        ws.append(row)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


class ReportService:

    # ---------------- Customer report ----------------

    @staticmethod
    def _customer_row(c, directory):
        return {
            "id": c.id,
            "name": " ".join(p for p in [c.first_name, c.middle_name, c.last_name] if p),
            "mobile_number": c.mobile_number,
            "email": c.email,
            "district": c.district,
            "assigned_staff_id": c.assigned_staff_id,
            "assigned_staff_name": _staff_name(directory, c.assigned_staff_id),
            "status": c.customer_status,
            "is_active": c.is_active,
            "registered_on": c.created_at
        }

    @staticmethod
    async def customer_report(
        db: Session,
        token: str,
        district: str | None,
        staff_id: UUID | None,
        customer_status: str | None,
        is_active: bool | None,
        product_id: UUID | None,
        registration_date_from: date | None,
        registration_date_to: date | None,
        sort_by: str,
        sort_order: str,
        limit: int,
        offset: int
    ):
        current_user = current_user_context.get()
        directory = await staff_service.get_staff_directory(current_user, token)

        result = report_repository.customer_report(
            db=db,
            district=district,
            staff_id=staff_id,
            customer_status=customer_status,
            is_active=is_active,
            product_id=product_id,
            registration_date_from=registration_date_from,
            registration_date_to=registration_date_to,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset
        )

        items = [ReportService._customer_row(c, directory) for c in result["items"]]

        return {"items": items, "total": result["total"]}

    @staticmethod
    async def customer_report_export(
        db: Session,
        token: str,
        district: str | None,
        staff_id: UUID | None,
        customer_status: str | None,
        is_active: bool | None,
        product_id: UUID | None,
        registration_date_from: date | None,
        registration_date_to: date | None,
        sort_by: str,
        sort_order: str
    ):
        current_user = current_user_context.get()
        directory = await staff_service.get_staff_directory(current_user, token)

        result = report_repository.customer_report(
            db=db,
            district=district,
            staff_id=staff_id,
            customer_status=customer_status,
            is_active=is_active,
            product_id=product_id,
            registration_date_from=registration_date_from,
            registration_date_to=registration_date_to,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=None,
            offset=None
        )

        headers = [
            "Customer Name", "Mobile Number", "Email ID", "District",
            "Assigned Staff", "Status", "Active/Inactive", "Registered On"
        ]

        rows = []
        for c in result["items"]:
            row = ReportService._customer_row(c, directory)
            rows.append([
                row["name"],
                row["mobile_number"],
                row["email"],
                row["district"],
                row["assigned_staff_name"],
                row["status"],
                "Active" if row["is_active"] else "Inactive",
                _format_date(row["registered_on"])
            ])

        return _excel_response(headers, rows, "customer_report.xlsx")

    # ---------------- Product report ----------------

    @staticmethod
    def _product_row(p, total_customers, last_purchase_date):
        return {
            "id": p.id,
            "product_code": p.product_code,
            "product_name": p.product_name,
            "product_description": p.product_description,
            "total_customers": total_customers or 0,
            "last_purchase_date": last_purchase_date
        }

    @staticmethod
    def product_report(
        db: Session,
        product_id: UUID | None,
        purchase_date_from: date | None,
        purchase_date_to: date | None,
        sort_by: str,
        sort_order: str,
        limit: int,
        offset: int
    ):
        result = report_repository.product_report(
            db=db,
            product_id=product_id,
            purchase_date_from=purchase_date_from,
            purchase_date_to=purchase_date_to,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset
        )

        items = [
            ReportService._product_row(p, total, last)
            for p, total, last in result["items"]
        ]

        return {"items": items, "total": result["total"]}

    @staticmethod
    def product_report_export(
        db: Session,
        product_id: UUID | None,
        purchase_date_from: date | None,
        purchase_date_to: date | None,
        sort_by: str,
        sort_order: str
    ):
        result = report_repository.product_report(
            db=db,
            product_id=product_id,
            purchase_date_from=purchase_date_from,
            purchase_date_to=purchase_date_to,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=None,
            offset=None
        )

        headers = [
            "Product Code", "Product Name", "Product Description",
            "Total Customers", "Last Purchase Date"
        ]

        rows = []
        for p, total, last in result["items"]:
            row = ReportService._product_row(p, total, last)
            rows.append([
                row["product_code"],
                row["product_name"],
                row["product_description"],
                row["total_customers"],
                _format_date(row["last_purchase_date"])
            ])

        return _excel_response(headers, rows, "product_report.xlsx")

    # ---------------- Follow-up report ----------------

    @staticmethod
    def _follow_up_row(c, f, directory):
        return {
            "customer_id": c.id,
            "name": " ".join(p for p in [c.first_name, c.middle_name, c.last_name] if p),
            "mobile_number": c.mobile_number,
            "status": f.status.value if hasattr(f.status, "value") else f.status,
            "assigned_staff_id": c.assigned_staff_id,
            "assigned_staff_name": _staff_name(directory, c.assigned_staff_id),
            "latest_remarks": f.description,
            "remarks_date": f.current_date
        }

    @staticmethod
    async def follow_up_report(
        db: Session,
        token: str,
        product_id: UUID | None,
        follow_up_status: str | None,
        staff_id: UUID | None,
        date_from: date | None,
        date_to: date | None,
        sort_by: str,
        sort_order: str,
        limit: int,
        offset: int
    ):
        current_user = current_user_context.get()
        directory = await staff_service.get_staff_directory(current_user, token)

        result = report_repository.follow_up_report(
            db=db,
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

        items = [
            ReportService._follow_up_row(c, f, directory)
            for c, f in result["items"]
        ]

        return {"items": items, "total": result["total"]}

    @staticmethod
    async def follow_up_report_export(
        db: Session,
        token: str,
        product_id: UUID | None,
        follow_up_status: str | None,
        staff_id: UUID | None,
        date_from: date | None,
        date_to: date | None,
        sort_by: str,
        sort_order: str
    ):
        current_user = current_user_context.get()
        directory = await staff_service.get_staff_directory(current_user, token)

        result = report_repository.follow_up_report(
            db=db,
            product_id=product_id,
            follow_up_status=follow_up_status,
            staff_id=staff_id,
            date_from=date_from,
            date_to=date_to,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=None,
            offset=None
        )

        headers = [
            "Customer Name", "Mobile Number", "Follow-Up Status",
            "Assigned Staff", "Latest Remarks", "Remarks Date"
        ]

        rows = []
        for c, f in result["items"]:
            row = ReportService._follow_up_row(c, f, directory)
            rows.append([
                row["name"],
                row["mobile_number"],
                row["status"],
                row["assigned_staff_name"],
                row["latest_remarks"],
                _format_date(row["remarks_date"])
            ])

        return _excel_response(headers, rows, "follow_up_report.xlsx")


report_service = ReportService()
