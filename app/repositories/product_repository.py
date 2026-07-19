from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self):
        super().__init__(Product)

    def search(
        self,
        db: Session,
        search: str,
        limit: int,
        offset: int
    ):

        query = (
            db.query(Product)
            .filter(
                Product.is_deleted == False
            )
        )

        if search:
            query = query.filter(
                or_(
                    Product.product_name.ilike(f"%{search}%"),
                    Product.product_code.ilike(f"%{search}%")
                )
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

    def get_by_code(
        self,
        db: Session,
        product_code: str
    ):

        return (
            db.query(Product)
            .filter(
                Product.product_code == product_code,
                Product.is_deleted == False
            )
            .first()
        )


product_repository = ProductRepository()
