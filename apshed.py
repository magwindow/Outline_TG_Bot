from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.models import async_session, OutlineKey
from sqlalchemy import select
import logging


async def notify_expiring_keys(bot):
    """Проверка и напоминание о ключах, срок действия которых подходит к концу."""
    async with async_session() as session:
        result = await session.execute(
            select(OutlineKey).where(
                OutlineKey.created_at <= datetime.utcnow() - timedelta(days=30)
            )
        )
        expiring_keys = result.scalars().all()

        for key in expiring_keys:
            try:
                await bot.send_message(chat_id=key.chat_id,
                                       text=f"⏰ Напоминание: срок действия ключа `{key.key_id}` скоро закончится.")
            except Exception as e:
                logging.error(f"Ошибка при отправке уведомления: {e}")


def start_scheduler(bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: notify_expiring_keys(bot), CronTrigger(hour=10, minute=0))  # Каждый день в 10:00
    scheduler.start()
