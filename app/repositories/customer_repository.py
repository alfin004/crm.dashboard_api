from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):

    def __init__(self):
        super().__init__(Customer)

    def search(
        self,
        db: Session,
        search: str,
        limit: int,
        offset: int
    ):

        query = (
            db.query(Customer)
            .filter(
                Customer.is_deleted == False
            )
        )

        if search:
            query = query.filter(
                or_(
                    Customer.first_name.ilike(f"%{search}%"),
                    Customer.last_name.ilike(f"%{search}%"),
                    Customer.email.ilike(f"%{search}%"),
                    Customer.mobile_number.ilike(f"%{search}%")
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


customer_repository = CustomerRepository()