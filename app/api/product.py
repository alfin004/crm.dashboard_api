from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.core.response import success_response

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(get_current_user)]
)


@router.post("")
async def create_product(
        request: ProductCreate,
        db: Session = Depends(get_db)
):
    product = ProductService.create(
        db,
        request
    )

    return success_response(product)


@router.get("")
async def get_products(
        limit: int = 10,
        offset: int = 0,
        search: str = None,
        db: Session = Depends(get_db)):

    products = ProductService.get_all(
        db,
        limit,
        offset,
        search
    )

    return success_response(products)


@router.get("/{product_id}")
async def get_product(
        product_id,
        db: Session = Depends(get_db)):

    product = ProductService.get_by_id(
        db,
        product_id
    )

    return success_response(product)


@router.put("/{product_id}")
async def update_product(
        product_id,
        request: ProductUpdate,
        db: Session = Depends(get_db)):

    product = ProductService.update(
        db,
        product_id,
        request
    )

    return success_response(
        product,
        "Updated successfully"
    )


@router.delete("/{product_id}")
async def delete_product(
        product_id,
        db: Session = Depends(get_db)):

    ProductService.delete(
        db,
        product_id
    )

    return success_response(
        None,
        "Deleted successfully"
    )
