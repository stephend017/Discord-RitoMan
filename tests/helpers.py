from unittest.mock import MagicMock, AsyncMock


def discord_ctx_mock() -> MagicMock:
    """
    Returns the ctx object passed to each bot command funciton

    Returns:
        MagicMock: A magic mock that mocks the context object
    """
    ctx = MagicMock()
    ctx.send = AsyncMock()
    return ctx
