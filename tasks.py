import asyncio
from datetime import datetime

from sqlalchemy import select
from database.models import async_session, OutlineKey
from outline_service import delete_key


async def cleanup_expired_keys():
    while True:
        print("🔍 Проверка просроченных ключей...")
        async with async_session() as session:
            result = await session.execute(
                select(OutlineKey).where(
                    OutlineKey.expires_at != None,
                    OutlineKey.expires_at < datetime.utcnow()
                )
            )
            expired_keys = result.scalars().all()

            for key in expired_keys:
                success = delete_key(key.key_id)
                if success:
                    await session.delete(key)
                    print(f"🗑 Ключ {key.key_id} удалён.")
            await session.commit()

        await asyncio.sleep(3600)  # Проверка каждый час
