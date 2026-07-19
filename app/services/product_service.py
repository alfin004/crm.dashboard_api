from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.context import current_user_context
from app.models.product import Product
from app.repositories.product_repository import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create(
        db: Session,
        request: ProductCreate
    ):
        current_user = current_user_context.get()

        existing = product_repository.get_by_code(
            db,
            request.product_code
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product code already exists"
            )

        product = Product(
            **request.model_dump(),
            created_by=current_user["id"]
        )

        return product_repository.create(
            db,
            product
        )

    @staticmethod
    def get_all(
        db: Session,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None
    ):
        if search:
            return product_repository.search(
                db=db,
                search=search,
                limit=limit,
                offset=offset
            )

        return product_repository.get_all(
            db=db,
            limit=limit,
            offset=offset
        )

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: UUID
    ):
        product = product_repository.get_by_id(
            db,
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return product

    @staticmethod
    def update(
        db: Session,
        product_id: UUID,
        request: ProductUpdate
    ):
        product = product_repository.get_by_id(
            db,
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        return product_repository.update(
            db,
            product,
            update_data
        )

    @staticmethod
    def delete(
        db: Session,
        product_id: UUID
    ):
        product = product_repository.get_by_id(
            db,
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        product_repository.delete(
            db,
            product
        )

        return {
            "success": True,
            "message": "Product deleted successfully"
        }


product_service = ProductService()
