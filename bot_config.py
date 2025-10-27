from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout

def create_bot_session():
    """Создать сессию с увеличенными таймаутами"""
    timeout = ClientTimeout(
        total=60,      # Общий таймаут 60 секунд
        connect=30,    # Таймаут соединения 30 секунд
        sock_read=30,  # Таймаут чтения сокета 30 секунд
        sock_connect=30  # Таймаут подключения сокета 30 секунд
    )
    
    return AiohttpSession(timeout=timeout)
