from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.context import current_user_context
from app.models.customer import Customer
from app.repositories.customer_repository import customer_repository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:

    @staticmethod
    def create(
        db: Session,
        request: CustomerCreate
    ):
        current_user = current_user_context.get()

        customer = Customer(
            **request.model_dump(),
            assigned_staff_id = current_user["id"],
            created_by=current_user["id"]
        )

        return customer_repository.create(
            db,
            customer
        )

    @staticmethod
    def get_all(
        db: Session,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None
    ):
        if search:
            return customer_repository.search(
                db=db,
                search=search,
                limit=limit,
                offset=offset
            )

        return customer_repository.get_all(
            db=db,
            limit=limit,
            offset=offset
        )

    @staticmethod
    def get_by_id(
        db: Session,
        customer_id: UUID
    ):
        customer = customer_repository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return customer

    @staticmethod
    def update(
        db: Session,
        customer_id: UUID,
        request: CustomerUpdate
    ):
        customer = customer_repository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        return customer_repository.update(
            db,
            customer,
            update_data
        )

    @staticmethod
    def delete(
        db: Session,
        customer_id: UUID
    ):
        customer = customer_repository.get_by_id(
            db,
            customer_id
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        customer_repository.delete(
            db,
            customer
        )

        return {
            "success": True,
            "message": "Customer deleted successfully"
        }


customer_service = CustomerService()