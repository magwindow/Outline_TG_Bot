import os
import json
from datetime import datetime, timedelta

import aiohttp
import requests
from aiogram.types import Message
from urllib3.exceptions import InsecureRequestWarning
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import OutlineKey
from key import Key
from dotenv import find_dotenv, load_dotenv

from keyboards.inline_keyboard import main_keyboard

load_dotenv(find_dotenv())

api_url = os.getenv('API_URL')
session = requests.Session()


# Декоратор для создания ключа и обработки ошибок
def create_key_decorator(limit=None, days_valid=None):
    def decorator(func):
        async def wrapper(chat, key_name, db_session: AsyncSession):
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            url = f"{api_url}/access-keys"
            error_message = ''
            r = requests.post(url, verify=False)  # Создаем новый ключ

            if r.status_code >= 400:
                return f"Что-то пошло не так.\nНе получилось создать ключ. Статус запроса: {r.status_code}"

            response = json.loads(r.text)
            key_id = response.get('id')
            access_url = response.get('accessUrl')

            # Переименование ключа
            rename_url = f"{api_url}/access-keys/{key_id}/name"
            r = requests.put(rename_url, data={'name': key_name}, verify=False)

            if r.status_code >= 400:
                error_message = f"Ключ создан, но не получилось его переименовать. Статус запроса: {r.status_code}"

            # Применяем ограничение, если оно задано
            if limit is not None:
                add_data_limit(key_id, limit)

            # Расчет срока действия
            expires_at = None
            if days_valid is not None:
                expires_at = datetime.utcnow() + timedelta(days=days_valid)

            # Записываем ключ в базу данных
            outline_key = OutlineKey(
                key_id=key_id,
                access_url=access_url,
                user_name=key_name,
                chat_id=chat.id,
                total_limit_gb=round(limit / 1000 / 1000 / 1000, 2) if limit else 0,
                expires_at=expires_at
            )
            db_session.add(outline_key)
            await db_session.commit()  # Сохраняем запись в БД

            return Key(key_id, key_name, access_url, error_message)

        return wrapper

    return decorator


def add_data_limit(key_id, limit_bytes):
    """Устанавливает ограничение на количество байт в ключе"""
    data = {"limit": {"bytes": limit_bytes}}
    response = session.put(f"{api_url}/access-keys/{key_id}/data-limit", json=data, verify=False)
    if response.status_code != 204:
        print(f"❗️Не удалось установить лимит на ключ {key_id}, статус: {response.status_code}")
    return response.status_code == 204


def delete_key(key_id: str) -> bool:
    url = f"{api_url}/access-keys/{key_id}"
    response = requests.delete(url, verify=False)
    return response.status_code == 204


# Определяем функции с использованием декоратора
@create_key_decorator(limit=10 * 1000 ** 3, days_valid=3)  # Пробный: 10 ГБ, 3 дня
def create_new_key_trial(chat, key_name, db_session: AsyncSession):
    pass


@create_key_decorator(limit=100 * 1000 ** 3, days_valid=30)  # Месяц: 100 ГБ
def create_new_key_100(chat, key_name, db_session: AsyncSession):
    pass


@create_key_decorator(limit=300 * 1000 ** 3, days_valid=90)  # 3 месяца: 300 ГБ
def create_new_key_300(chat, key_name, db_session: AsyncSession):
    pass


@create_key_decorator(limit=600 * 1000 ** 3, days_valid=180)  # 6 месяцев: 600 ГБ
def create_new_key_600(chat, key_name, db_session: AsyncSession):
    pass


@create_key_decorator(days_valid=365)  # Безлимит: 1 год
def create_new_key_no_limit(chat, key_name, db_session: AsyncSession):
    pass


async def get_key_traffic_async(key_id: str) -> float:
    """
    Возвращает объем использованного трафика в ГБ для указанного ключа
    """
    url = f"{api_url}/metrics/transfer"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            if response.status != 200:
                print(f"❌ Ошибка запроса: {response.status}")
                return 0.0
            data = await response.json()
            print(f"📊 Данные по трафику: {data}")
            traffic_data = data.get("bytesTransferredByUserId", {})
            bytes_used = traffic_data.get(key_id, 0)

            if bytes_used == 0:
                print(f"⚠️ Нет трафика для ключа ID: {key_id}")

            return round(bytes_used / 1024 / 1024 / 1024, 2)


async def handle_invite(message: Message):
    bot_username = "tadivpn_bot"  # можно вынести в .env при желании
    user_id = message.from_user.id
    invite_url = f"https://t.me/{bot_username}?start={user_id}"

    await message.answer(
        f"🔗 Пригласи друга и получи бонус!\n"
        f"Просто отправь ему эту ссылку:\n\n{invite_url}",
        reply_markup=main_keyboard()
    )
