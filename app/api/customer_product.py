from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.services.customer_product_service import CustomerProductService
from app.core.response import success_response

router = APIRouter(
    tags=["Customer-Product Assignments"],
    dependencies=[Depends(get_current_user)]
)


# --- Product-first routes (matches: product list -> "Assign Customer" button) ---

@router.post("/products/{product_id}/customers/{customer_id}")
async def assign_customer_to_product(
        product_id,
        customer_id,
        db: Session = Depends(get_db)):

    assignment = CustomerProductService.assign(
        db,
        customer_id,
        product_id
    )

    return success_response(assignment, "Customer assigned successfully")


@router.delete("/products/{product_id}/customers/{customer_id}")
async def unassign_customer_from_product(
        product_id,
        customer_id,
        db: Session = Depends(get_db)):

    result = CustomerProductService.unassign(
        db,
        customer_id,
        product_id
    )

    return success_response(None, result["message"])


@router.get("/products/{product_id}/customers")
async def get_product_customers(
        product_id,
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db)):

    customers = CustomerProductService.get_customers_for_product(
        db,
        product_id,
        limit,
        offset
    )

    return success_response(customers)


# --- Customer-first routes (for the customer detail page) ---

@router.post("/customers/{customer_id}/products/{product_id}")
async def assign_product_to_customer(
        customer_id,
        product_id,
        db: Session = Depends(get_db)):

    assignment = CustomerProductService.assign(
        db,
        customer_id,
        product_id
    )

    return success_response(assignment, "Product assigned successfully")


@router.delete("/customers/{customer_id}/products/{product_id}")
async def unassign_product_from_customer(
        customer_id,
        product_id,
        db: Session = Depends(get_db)):

    result = CustomerProductService.unassign(
        db,
        customer_id,
        product_id
    )

    return success_response(None, result["message"])


@router.get("/customers/{customer_id}/products")
async def get_customer_products(
        customer_id,
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db)):

    products = CustomerProductService.get_products_for_customer(
        db,
        customer_id,
        limit,
        offset
    )

    return success_response(products)
