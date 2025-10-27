import os
from typing import Optional

# Конфигурация
API_TOKEN = ""
GPT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
GPT_TOKEN = ""
GPT_MODEL = "gpt-4o-mini"
DEEPSEEK_API_KEY = ""
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat" 

# AI агент - виртуальный ID (будет выглядеть как обычный участник)
AI_AGENT_VIRTUAL_ID = 1  # Можно изменить на любой номер

# Реальный ID агента для внутренней логики
AI_AGENT_REAL_ID = -1

# Admin ID для доступа к консоли
ADMIN_ID = 123456789  # Ваш Telegram ID