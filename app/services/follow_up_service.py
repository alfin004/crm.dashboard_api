from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.context import current_user_context
from app.models.customer_follow_up import CustomerFollowUp
from app.repositories.customer_repository import customer_repository
from app.repositories.follow_up_repository import follow_up_repository
from app.schemas.follow_up import FollowUpCreate


class FollowUpService:

    @staticmethod
    def create(
        db: Session,
        customer_id: UUID,
        request: FollowUpCreate
    ):
        current_user = current_user_context.get()

        customer = customer_repository.get_by_id(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        data = request.model_dump()
        if not data.get("current_date"):
            data["current_date"] = date.today()

        follow_up = CustomerFollowUp(
            **data,
            customer_id=customer_id,
            followed_up_by=current_user["id"]
        )

        follow_up = follow_up_repository.create(db, follow_up)

        # Keep the customer's headline status in sync with their latest follow-up
        customer_repository.update(
            db,
            customer,
            {"customer_status": request.status.value}
        )

        return follow_up

    @staticmethod
    def get_history(
        db: Session,
        customer_id: UUID,
        limit: int = 10,
        offset: int = 0
    ):
        customer = customer_repository.get_by_id(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return follow_up_repository.get_by_customer(db, customer_id, limit, offset)

    @staticmethod
    def get_latest(
        db: Session,
        customer_id: UUID
    ):
        customer = customer_repository.get_by_id(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        latest = follow_up_repository.get_latest(db, customer_id)

        if not latest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No follow-up records found for this customer"
            )

        return latest


follow_up_service = FollowUpService()
