from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import dashboard_repository


class DashboardService:
    @staticmethod
    def get_staff_performance(db: Session, sort_by: str = "customer"):
        rows = dashboard_repository.get_staff_performance(db, sort_by)

        return [
            {
                "staff_id": row.id,
                "staff_name": row.username,
                "customer_count": row.customer_count,
                "follow_up_count": row.follow_up_count,
            }
            for row in rows
        ]


dashboard_service = DashboardService()
