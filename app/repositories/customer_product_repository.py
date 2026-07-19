from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.customer_product import CustomerProduct
from app.repositories.base_repository import BaseRepository


class CustomerProductRepository(BaseRepository[CustomerProduct]):

    def __init__(self):
        super().__init__(CustomerProduct)

    def get_active_assignment(
        self,
        db: Session,
        customer_id,
        product_id
    ):

        return (
            db.query(CustomerProduct)
            .filter(
                CustomerProduct.customer_id == customer_id,
                CustomerProduct.product_id == product_id,
                CustomerProduct.is_deleted == False
            )
            .first()
        )

    def get_products_for_customer(
        self,
        db: Session,
        customer_id,
        limit: int = 10,
        offset: int = 0
    ):

        query = (
            db.query(Product)
            .join(CustomerProduct, CustomerProduct.product_id == Product.id)
            .filter(
                CustomerProduct.customer_id == customer_id,
                CustomerProduct.is_deleted == False,
                Product.is_deleted == False
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

    def get_customers_for_product(
        self,
        db: Session,
        product_id,
        limit: int = 10,
        offset: int = 0
    ):

        query = (
            db.query(Customer)
            .join(CustomerProduct, CustomerProduct.customer_id == Customer.id)
            .filter(
                CustomerProduct.product_id == product_id,
                CustomerProduct.is_deleted == False,
                Customer.is_deleted == False
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


customer_product_repository = CustomerProductRepository()
