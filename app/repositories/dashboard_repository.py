from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_follow_up import CustomerFollowUp
from app.models.user import User


class DashboardRepository:
    def get_staff_performance(self, db: Session, sort_by: str = "customer"):
        """Return every staff user, including those with no CRM assignments."""
        customer_count = func.count(func.distinct(Customer.id)).label("customer_count")
        follow_up_count = func.count(func.distinct(CustomerFollowUp.id)).label(
            "follow_up_count"
        )

        query = (
            db.query(User.id, User.username, customer_count, follow_up_count)
            .outerjoin(
                Customer,
                and_(
                    Customer.assigned_staff_id == User.id,
                    Customer.is_deleted == False,
                ),
            )
            .outerjoin(
                CustomerFollowUp,
                and_(
                    CustomerFollowUp.followed_up_by == User.id,
                    CustomerFollowUp.is_deleted == False,
                ),
            )
            # Roles are stored as strings; normalizing makes USER/user work alike.
            # .filter(func.lower(User.role) == "user")
            .group_by(User.id, User.username)
        )

        sort_column = follow_up_count if sort_by == "follow_up" else customer_count
        return query.order_by(desc(sort_column), User.username.asc()).all()


dashboard_repository = DashboardRepository()
