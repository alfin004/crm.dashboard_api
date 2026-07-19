import httpx

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.context import current_user_context

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{settings.AUTH_BASE_URL}/auth/me",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        if response.status_code == 200:
            user = response.json()

            # Store in context variable
            current_user_context.set(user)

            return user

        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service unavailable"
        )