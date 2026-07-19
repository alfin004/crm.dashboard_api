from datetime import date
from uuid import UUID

from sqlalchemy import asc, desc, func, and_
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.customer_product import CustomerProduct
from app.models.customer_follow_up import CustomerFollowUp


class ReportRepository:

    # ---------------- Customer report ----------------

    def customer_report(
        self,
        db: Session,
        district: str | None = None,
        staff_id: UUID | None = None,
        customer_status: str | None = None,
        is_active: bool | None = None,
        product_id: UUID | None = None,
        registration_date_from: date | None = None,
        registration_date_to: date | None = None,
        sort_by: str = "registered_on",
        sort_order: str = "desc",
        limit: int | None = 10,
        offset: int | None = 0
    ):
        query = db.query(Customer).filter(Customer.is_deleted == False)

        if district:
            query = query.filter(Customer.district == district)

        if staff_id:
            query = query.filter(Customer.assigned_staff_id == staff_id)

        if customer_status:
            query = query.filter(Customer.customer_status == customer_status)

        if is_active is not None:
            query = query.filter(Customer.is_active == is_active)

        if product_id:
            query = query.join(
                CustomerProduct,
                and_(
                    CustomerProduct.customer_id == Customer.id,
                    CustomerProduct.product_id == product_id,
                    CustomerProduct.is_deleted == False
                )
            )

        if registration_date_from:
            query = query.filter(func.date(Customer.created_at) >= registration_date_from)

        if registration_date_to:
            query = query.filter(func.date(Customer.created_at) <= registration_date_to)

        sort_map = {
            "name": Customer.first_name,
            "district": Customer.district,
            "status": Customer.customer_status,
            "is_active": Customer.is_active,
            "registered_on": Customer.created_at
        }
        sort_column = sort_map.get(sort_by, Customer.created_at)
        query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

        total = query.count()

        if limit is not None:
            query = query.offset(offset or 0).limit(limit)

        return {
            "items": query.all(),
            "total": total
        }

    # ---------------- Product report ----------------

    def product_report(
        self,
        db: Session,
        product_id: UUID | None = None,
        purchase_date_from: date | None = None,
        purchase_date_to: date | None = None,
        sort_by: str = "product_name",
        sort_order: str = "asc",
        limit: int | None = 10,
        offset: int | None = 0
    ):
        join_conditions = [
            CustomerProduct.product_id == Product.id,
            CustomerProduct.is_deleted == False
        ]

        if purchase_date_from:
            join_conditions.append(func.date(CustomerProduct.created_at) >= purchase_date_from)

        if purchase_date_to:
            join_conditions.append(func.date(CustomerProduct.created_at) <= purchase_date_to)

        query = (
            db.query(
                Product,
                func.count(func.distinct(CustomerProduct.customer_id)).label("total_customers"),
                func.max(CustomerProduct.created_at).label("last_purchase_date")
            )
            .outerjoin(CustomerProduct, and_(*join_conditions))
            .filter(Product.is_deleted == False)
        )

        if product_id:
            query = query.filter(Product.id == product_id)

        query = query.group_by(Product.id)

        sort_map = {
            "product_code": Product.product_code,
            "product_name": Product.product_name,
            "total_customers": func.count(func.distinct(CustomerProduct.customer_id)),
            "last_purchase_date": func.max(CustomerProduct.created_at)
        }
        sort_column = sort_map.get(sort_by, Product.product_name)
        query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

        total = query.count()

        if limit is not None:
            query = query.offset(offset or 0).limit(limit)

        return {
            "items": query.all(),
            "total": total
        }

    # ---------------- Follow-up report ----------------

    def follow_up_report(
        self,
        db: Session,
        product_id: UUID | None = None,
        follow_up_status: str | None = None,
        staff_id: UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        sort_by: str = "remarks_date",
        sort_order: str = "desc",
        limit: int | None = 10,
        offset: int | None = 0
    ):
        latest_sq = (
            db.query(
                CustomerFollowUp.customer_id.label("customer_id"),
                func.max(CustomerFollowUp.created_at).label("latest_at")
            )
            .filter(CustomerFollowUp.is_deleted == False)
            .group_by(CustomerFollowUp.customer_id)
            .subquery()
        )

        query = (
            db.query(Customer, CustomerFollowUp)
            .join(latest_sq, latest_sq.c.customer_id == Customer.id)
            .join(
                CustomerFollowUp,
                and_(
                    CustomerFollowUp.customer_id == latest_sq.c.customer_id,
                    CustomerFollowUp.created_at == latest_sq.c.latest_at,
                    CustomerFollowUp.is_deleted == False
                )
            )
            .filter(Customer.is_deleted == False)
        )

        if product_id:
            query = query.join(
                CustomerProduct,
                and_(
                    CustomerProduct.customer_id == Customer.id,
                    CustomerProduct.product_id == product_id,
                    CustomerProduct.is_deleted == False
                )
            )

        if follow_up_status:
            query = query.filter(CustomerFollowUp.status == follow_up_status)

        if staff_id:
            query = query.filter(Customer.assigned_staff_id == staff_id)

        if date_from:
            query = query.filter(CustomerFollowUp.current_date >= date_from)

        if date_to:
            query = query.filter(CustomerFollowUp.current_date <= date_to)

        sort_map = {
            "customer_name": Customer.first_name,
            "status": CustomerFollowUp.status,
            "remarks_date": CustomerFollowUp.current_date
        }
        sort_column = sort_map.get(sort_by, CustomerFollowUp.current_date)
        query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

        total = query.count()

        if limit is not None:
            query = query.offset(offset or 0).limit(limit)

        return {
            "items": query.all(),
            "total": total
        }


report_repository = ReportRepository()
