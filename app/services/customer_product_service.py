from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.context import current_user_context
from app.models.customer_product import CustomerProduct
from app.repositories.customer_product_repository import customer_product_repository
from app.repositories.customer_repository import customer_repository
from app.repositories.product_repository import product_repository


def _customer_brief(customer):
    name = " ".join(
        part for part in [customer.first_name, customer.middle_name, customer.last_name]
        if part
    )

    place = ", ".join(
        part for part in [customer.district, customer.state]
        if part
    )

    return {
        "id": customer.id,
        "name": name,
        "email": customer.email,
        "phone_number": customer.mobile_number,
        "place": place
    }


def _product_brief(product):
    return {
        "id": product.id,
        "product_code": product.product_code,
        "product_name": product.product_name,
        "status": product.status
    }


class CustomerProductService:

    @staticmethod
    def assign(
        db: Session,
        customer_id: UUID,
        product_id: UUID
    ):
        current_user = current_user_context.get()

        customer = customer_repository.get_by_id(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        product = product_repository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        existing = customer_product_repository.get_active_assignment(
            db,
            customer_id,
            product_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already assigned to this customer"
            )

        assignment = CustomerProduct(
            customer_id=customer_id,
            product_id=product_id,
            assigned_staff_id=current_user["id"]
        )

        return customer_product_repository.create(db, assignment)

    @staticmethod
    def unassign(
        db: Session,
        customer_id: UUID,
        product_id: UUID
    ):
        assignment = customer_product_repository.get_active_assignment(
            db,
            customer_id,
            product_id
        )

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )

        customer_product_repository.delete(db, assignment)

        return {
            "success": True,
            "message": "Product unassigned successfully"
        }

    @staticmethod
    def get_products_for_customer(
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

        result = customer_product_repository.get_products_for_customer(
            db,
            customer_id,
            limit,
            offset
        )

        return {
            "items": [_product_brief(p) for p in result["items"]],
            "total": result["total"]
        }

    @staticmethod
    def get_customers_for_product(
        db: Session,
        product_id: UUID,
        limit: int = 10,
        offset: int = 0
    ):
        product = product_repository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        result = customer_product_repository.get_customers_for_product(
            db,
            product_id,
            limit,
            offset
        )

        return {
            "items": [_customer_brief(c) for c in result["items"]],
            "total": result["total"]
        }


customer_product_service = CustomerProductService()
