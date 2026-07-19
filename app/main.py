from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api.customer import router as customer_router
from app.api.product import router as product_router
from app.api.customer_product import router as customer_product_router
from app.api.follow_up import router as follow_up_router
from app.api.report import router as report_router
from app.api.staff import router as staff_router

from app.models.customer import Customer
from app.models.product import Product
from app.models.customer_product import CustomerProduct
from app.models.customer_follow_up import CustomerFollowUp

from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(product_router)
app.include_router(customer_product_router)
app.include_router(follow_up_router)
app.include_router(report_router)
app.include_router(staff_router)
