from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.follow_up import FollowUpCreate
from app.services.follow_up_service import FollowUpService
from app.core.response import success_response

router = APIRouter(
    tags=["Follow-ups"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/customers/{customer_id}/follow-ups")
async def create_follow_up(
        customer_id,
        request: FollowUpCreate,
        db: Session = Depends(get_db)):

    follow_up = FollowUpService.create(
        db,
        customer_id,
        request
    )

    return success_response(follow_up, "Follow-up recorded successfully")


@router.get("/customers/{customer_id}/follow-ups")
async def get_follow_up_history(
        customer_id,
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db)):

    history = FollowUpService.get_history(
        db,
        customer_id,
        limit,
        offset
    )

    return success_response(history)


@router.get("/customers/{customer_id}/follow-ups/latest")
async def get_latest_follow_up(
        customer_id,
        db: Session = Depends(get_db)):

    latest = FollowUpService.get_latest(
        db,
        customer_id
    )

    return success_response(latest)
