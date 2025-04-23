from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import async_session, OutlineKey


class TrialAccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: CallbackQuery, data):
        # Проверяем только если пользователь жмёт на 'trial'
        if event.data != 'trial_outline':
            return await handler(event, data)

        user_id = event.from_user.id

        async with async_session() as session:  # Получаем сессию БД
            used_trial = await self.has_used_trial(session, user_id)

            if used_trial:
                await event.answer("Вы уже использовали бесплатный период.", show_alert=True)
                return

        # Если можно использовать пробный доступ — продолжаем выполнение
        return await handler(event, data)

    @staticmethod
    async def has_used_trial(session: AsyncSession, user_id: int) -> bool:
        result = await session.execute(
            # Предположим, в OutlineKey есть колонка chat_id
            OutlineKey.__table__.select().where(OutlineKey.chat_id == user_id)
        )
        keys = result.fetchall()
        return len(keys) > 0
