from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.customer import CustomerCreate,CustomerUpdate
from app.services.customer_service import CustomerService
from app.core.response import success_response

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(get_current_user)]
)


@router.post("")
async def create_customer(
        request: CustomerCreate,
        db: Session = Depends(get_db)
):
    customer = CustomerService.create(
        db,
        request  
    )

    return success_response(customer)

@router.get("")
async def get_customers(
        limit: int = 10,
        offset: int = 0,
        search: str = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        db: Session = Depends(get_db)):

    customers = CustomerService.get_all(
        db,
        limit,
        offset,
        search
        # sort_by,
        # sort_order
    )

    return success_response(customers)

@router.get("/{customer_id}")
async def get_customer(
        customer_id,
        db: Session = Depends(get_db)):

    customer = CustomerService.get_by_id(
        db,
        customer_id
    )

    return success_response(customer)

@router.put("/{customer_id}")
async def update_customer(
        customer_id,
        request: CustomerUpdate,
        db: Session = Depends(get_db)):

    customer = CustomerService.update(
        db,
        customer_id,
        request
    )

    return success_response(
        customer,
        "Updated successfully"
    )

@router.delete("/{customer_id}")
async def delete_customer(
        customer_id,
        db: Session = Depends(get_db)):

    CustomerService.delete(
        db,
        customer_id
    )

    return success_response(
        None,
        "Deleted successfully"
    )