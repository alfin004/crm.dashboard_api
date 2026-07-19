import httpx

from fastapi import HTTPException, status

from app.core.config import settings


def _display_name(user: dict) -> str | None:
    return (
        user.get("name")
        or user.get("full_name")
        or user.get("username")
        or user.get("email")
    )


class StaffService:

    @staticmethod
    async def get_staff_list(current_user: dict, token: str):
        """
        ADMIN: pulls the full user list from the auth service (/users) and
        returns everyone as {id, name}.
        Any other role: only their own {id, name} is returned, since a
        non-admin staff member should only see themselves in the dropdown.
        """
        role = str((current_user or {}).get("role", "")).upper()

        if role == "ADMIN":
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get(
                        f"{settings.AUTH_BASE_URL}/users",
                        headers={"Authorization": f"Bearer {token}"}
                    )
            except httpx.ConnectError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Auth service unavailable"
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text
                )

            users = response.json()

            return [
                {
                    "id": user.get("id"),
                    "name": _display_name(user)
                }
                for user in users["data"]
            ]

        return [
            {
                "id": (current_user or {}).get("id"),
                "name": _display_name(current_user or {})
            }
        ]

    @staticmethod
    async def get_staff_directory(current_user: dict, token: str) -> dict:
        """id -> name lookup map, used to resolve staff names inside reports.

        Note: for non-ADMIN users this directory only contains their own
        entry (see get_staff_list), so any other staff id referenced in a
        report row will fall back to the raw id rather than a resolved name.
        """
        staff_list = await StaffService.get_staff_list(current_user, token)

        return {
            s["id"]: s["name"]
            for s in staff_list
            if s.get("id")
        }


staff_service = StaffService()
