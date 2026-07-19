from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.context import current_user_context
from app.core.response import success_response
from app.dependencies.auth import get_current_user, security
from app.services.staff_service import staff_service

router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/dropdown")
async def get_staff_dropdown(
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    current_user = current_user_context.get()

    staff_list = await staff_service.get_staff_list(
        current_user,
        credentials.credentials
    )

    return success_response(staff_list)
