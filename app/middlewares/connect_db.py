from typing import Callable, Awaitable, Any, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
import aiosqlite


class ConnectDB(BaseMiddleware):
    def __init__(self, name: str):
        self.name = name

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ):
        event = cast(Update, event)
        async with aiosqlite.connect(f"app/db/{self.name}.db") as conn:
            data.update(conn=conn)
            return await handler(event, data)
