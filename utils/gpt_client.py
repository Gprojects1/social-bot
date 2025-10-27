import aiohttp
import asyncio
from typing import Optional
from config import DEEPSEEK_API_KEY, DEEPSEEK_ENDPOINT, DEEPSEEK_MODEL


async def gpt_request(prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
    """Отправить запрос к DeepSeek API с обработкой ошибок"""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500,
        "stream": False
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                DEEPSEEK_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                print(f"DeepSeek API Status: {resp.status}")
                
                if resp.status != 200:
                    error_text = await resp.text()
                    print(f"DeepSeek API Error ({resp.status}): {error_text}")
                    return None
                
                data = await resp.json()
                
                # Проверяем наличие ошибки в ответе
                if "error" in data:
                    print(f"DeepSeek API Error: {data['error']}")
                    return None
                
                # Проверяем структуру ответа (DeepSeek использует тот же формат что и OpenAI)
                if "choices" not in data or len(data["choices"]) == 0:
                    print(f"Unexpected DeepSeek response structure: {data}")
                    return None
                
                content = data["choices"][0]["message"]["content"]
                print(f"DeepSeek Response: {content[:100]}...")
                return content
                
    except asyncio.TimeoutError:
        print("DeepSeek request timeout")
        return None
    except aiohttp.ClientError as e:
        print(f"DeepSeek request network error: {e}")
        return None
    except Exception as e:
        print(f"DeepSeek request unexpected error: {type(e).__name__}: {e}")
        return None


async def generate_action_text(action_name: str, action_desc: str, context: str) -> str:
    """Генерация текста действия агента через DeepSeek"""
    system_prompt = """Ты — студент в новом коллективе. 
Говори естественно, без формальностей. Не веди себя вежливо, веди себя нейтрально.
НЕ используй эмодзи, markdown и специальное форматирование.
Отвечай кратко — максимум 1-2 предложения."""
    
    prompt = f"""Ситуация: {context}

Твоё действие: {action_desc}

Что ты скажешь?"""
    
    response = await gpt_request(prompt, system_prompt)
    
    if not response:
        # Fallback на простые шаблоны
        fallbacks = {
            "ask_advice": "Подскажи, как лучше это сделать?",
            "share_joke": "Слушай, есть забавная история про это.",
            "support_idea": "Отличная мысль, я поддерживаю!",
            "give_guidance": "Давай я покажу, как это сделать правильно.",
            "demonstrate_superiority": "Я думаю, мой подход здесь эффективнее.",
            "set_shared_goal": "Предлагаю вместе поработать над этим.",
            "default": "Интересно, давайте обсудим это подробнее!"
        }
        return fallbacks.get(action_name, fallbacks["default"])
    
    return response.strip()
