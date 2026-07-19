from contextvars import ContextVar

current_user_context: ContextVar[dict | None] = ContextVar(
    "current_user_context",
    default=None
)