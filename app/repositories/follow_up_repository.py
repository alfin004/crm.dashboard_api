from sqlalchemy.orm import Session

from app.models.customer_follow_up import CustomerFollowUp
from app.repositories.base_repository import BaseRepository


class FollowUpRepository(BaseRepository[CustomerFollowUp]):

    def __init__(self):
        super().__init__(CustomerFollowUp)

    def get_by_customer(
        self,
        db: Session,
        customer_id,
        limit: int,
        offset: int
    ):

        query = (
            db.query(CustomerFollowUp)
            .filter(
                CustomerFollowUp.customer_id == customer_id,
                CustomerFollowUp.is_deleted == False
            )
            .order_by(CustomerFollowUp.created_at.desc())
        )

        total = query.count()

        data = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "items": data,
            "total": total
        }

    def get_latest(
        self,
        db: Session,
        customer_id
    ):

        return (
            db.query(CustomerFollowUp)
            .filter(
                CustomerFollowUp.customer_id == customer_id,
                CustomerFollowUp.is_deleted == False
            )
            .order_by(CustomerFollowUp.created_at.desc())
            .first()
        )


follow_up_repository = FollowUpRepository()
