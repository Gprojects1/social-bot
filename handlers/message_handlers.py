import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import numpy as np


from config import AI_AGENT_ID
from emotions.models import emotion_model, EMOTIONS, EMOTION_INDEX
from emotions.analyzer import analyze_emotion_vector
from moral_schemas.manager import MoralSchemaManager
from utils.gpt_client import generate_action_text, gpt_request


def extract_user_ids(text: str) -> list[int]:
    """Извлечь ID пользователей из текста сообщения"""
    patterns = [
        r'@id(-?\d+)',
        r'#id(-?\d+)',
        r'\bid(-?\d+)'
    ]
    
    user_ids = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            try:
                user_id = int(match)
                user_ids.append(user_id)
            except ValueError:
                continue
    
    return list(set(user_ids))  # Убираем дубликаты


def is_agent_mentioned(mentioned_ids: list[int]) -> bool:
    """Проверить, упомянут ли агент"""
    return AI_AGENT_ID in mentioned_ids


async def generate_simple_response(user_message: str) -> str:
    """Генерация простого ответа агента через DeepSeek"""
    system_prompt = """Ты — студент в новом коллективе. 
Говори естественно, без формальностей. Не веди себя вежливо, веди себя нейтрально.
НЕ используй эмодзи, markdown и специальное форматирование.
Отвечай кратко — максимум 1-2 предложения."""
    
    prompt = f"Пользователь написал: {user_message}\n\nТвой ответ:"
    
    response = await gpt_request(prompt, system_prompt)
    
    if not response:
        fallbacks = [
            "Спасибо, что написал!",
            "Интересная мысль, давай обсудим.",
            "Понял тебя, продолжай.",
        ]
        import random
        return random.choice(fallbacks)
    
    return response.strip()


async def process_message(user_id: int, text: str, emotion_vector: np.ndarray, chat_id: int, bot: Bot):
    """Обработать сообщение: обновить эмоции, проверить схемы, сгенерировать ответ"""
    
    print(f"\n{'='*70}")
    print(f"🔒 [ADMIN] Новое сообщение от User({user_id})")
    print(f"🔒 [ADMIN] Текст: {text[:100]}...")
    print(f"{'='*70}")
    
    # Извлекаем упоминания
    mentioned_ids = extract_user_ids(text)
    
    top_emotions = [(EMOTIONS[i], round(emotion_vector[i], 1)) for i in np.argsort(emotion_vector)[-5:] if emotion_vector[i] > 0]
    print(f"🔒 [ADMIN] 🧠 Распознанные эмоции: {top_emotions}")
    print(f"🔒 [ADMIN] 👥 Упоминания: {mentioned_ids if mentioned_ids else 'НЕТ'}")
    
    # Если нет упоминаний - игнорируем сообщение
    if not mentioned_ids:
        print(f"🔒 [ADMIN] ⚠️ Нет адресатов - сообщение игнорируется")
        print(f"{'='*70}\n")
        return
    
    # ШАГ 1: ОБНОВЛЯЕМ ЭМОЦИИ
    print(f"\n🔒 [ADMIN] === ШАГ 1: ОБНОВЛЕНИЕ ЭМОЦИЙ ===")
    
    for target_id in mentioned_ids:
        # 1.1 Обновляем отношение АВТОРА к АДРЕСАТУ (полная сила)
        print(f"🔒 [ADMIN] ⬆️ Обновление: User({user_id}) → User({target_id}) (коэф. 1.0)")
        emotion_model.update_relation(user_id, target_id, emotion_vector.tolist())
        
        current_rel = emotion_model.get_relation(user_id, target_id)
        top_rel = [(EMOTIONS[i], round(current_rel[i], 1)) for i in np.argsort(current_rel)[-5:] if current_rel[i] > 0]
        print(f"🔒 [ADMIN] 📊 Эмоции User({user_id}) → User({target_id}): {top_rel}")
        
        # 1.2 Обновляем отношение АДРЕСАТА к АВТОРУ (коэф. 0.5 - зеркальная реакция)
        mirrored_emotion_vector = emotion_vector * 0.5
        print(f"🔒 [ADMIN] ⬆️ Обновление (зеркало): User({target_id}) → User({user_id}) (коэф. 0.5)")
        emotion_model.update_relation(target_id, user_id, mirrored_emotion_vector.tolist())
        
        mirrored_rel = emotion_model.get_relation(target_id, user_id)
        top_mirrored = [(EMOTIONS[i], round(mirrored_rel[i], 1)) for i in np.argsort(mirrored_rel)[-5:] if mirrored_rel[i] > 0]
        print(f"🔒 [ADMIN] 📊 Эмоции User({target_id}) → User({user_id}): {top_mirrored}")
    
    # ШАГ 2: ПРОВЕРЯЕМ МОРАЛЬНЫЕ СХЕМЫ
    print(f"\n🔒 [ADMIN] === ШАГ 2: ПРОВЕРКА МОРАЛЬНЫХ СХЕМ ===")
    
    schema_manager = MoralSchemaManager()
    all_involved = [user_id] + mentioned_ids
    
    schema_activated = await schema_manager.check_and_activate_schemas(all_involved, chat_id, bot)
    
    # ШАГ 3: ЕСЛИ СХЕМА НЕ СРАБОТАЛА, НО ОБРАЩЕНИЕ К АГЕНТУ - ПРОСТОЙ ОТВЕТ
    if not schema_activated and is_agent_mentioned(mentioned_ids):
        print(f"\n🔒 [ADMIN] === ШАГ 3: ГЕНЕРАЦИЯ ПРОСТОГО ОТВЕТА ===")
        print(f"🔒 [ADMIN] 💬 Схемы не активированы, но есть обращение к агенту")
        print(f"🔒 [ADMIN] 🤖 Генерирую ответ через DeepSeek...")
        
        response_text = await generate_simple_response(text)
        
        if response_text:
            await bot.send_message(chat_id, response_text)
            print(f"🔒 [ADMIN] ✅ Агент ответил: {response_text[:50]}...")
            
            # Анализируем эмоции ответа агента
            response_emotion_vector = await analyze_emotion_vector(response_text)
            
            # Обновляем отношение АГЕНТА к ПОЛЬЗОВАТЕЛЮ (полная сила)
            print(f"🔒 [ADMIN] ⬆️ Обновление после ответа: AI({AI_AGENT_ID}) → User({user_id}) (коэф. 1.0)")
            emotion_model.update_relation(AI_AGENT_ID, user_id, response_emotion_vector.tolist())
            
            updated_rel = emotion_model.get_relation(AI_AGENT_ID, user_id)
            top_updated = [(EMOTIONS[i], round(updated_rel[i], 1)) for i in np.argsort(updated_rel)[-5:] if updated_rel[i] > 0]
            print(f"🔒 [ADMIN] 📊 Эмоции AI({AI_AGENT_ID}) → User({user_id}): {top_updated}")
            
            # Обновляем отношение ПОЛЬЗОВАТЕЛЯ к АГЕНТУ (коэф. 0.5 - реакция на ответ)
            mirrored_response = response_emotion_vector * 0.5
            print(f"🔒 [ADMIN] ⬆️ Обновление (реакция на ответ): User({user_id}) → AI({AI_AGENT_ID}) (коэф. 0.5)")
            emotion_model.update_relation(user_id, AI_AGENT_ID, mirrored_response.tolist())
            
            user_to_ai = emotion_model.get_relation(user_id, AI_AGENT_ID)
            top_user_to_ai = [(EMOTIONS[i], round(user_to_ai[i], 1)) for i in np.argsort(user_to_ai)[-5:] if user_to_ai[i] > 0]
            print(f"🔒 [ADMIN] 📊 Эмоции User({user_id}) → AI({AI_AGENT_ID}): {top_user_to_ai}")
    
    print(f"🔒 [ADMIN] === КОНЕЦ ОБРАБОТКИ ===\n")



async def setup_handlers(dp: Dispatcher, bot: Bot):
    """Настройка обработчиков сообщений"""
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await message.answer(
            "👋 Добро пожаловать в эксперимент.\n\n"
            "Общайтесь, упоминая других участников через @id123\n"
            "Чтобы обратиться ко мне: @id-1\n\n"
            "Команды:\n"
            "/help - справка\n"
            "/status - статус системы"
        )

    @dp.message(Command("help"))
    async def cmd_help(message: Message):
        await message.answer(
            "ℹ️ Как участвовать:\n\n"
            "1. Пишите сообщения\n"
            "2. Упоминайте участников: @id123\n"
            "3. Чтобы обратиться ко мне: @id-1\n"
            "4. Без упоминаний - сообщение игнорируется\n\n"
            "Примеры:\n"
            "@id123 привет!\n"
            "@id-1 помоги с задачей"
        )

    @dp.message(Command("status"))
    async def cmd_status(message: Message):
        await message.answer("✅ Система работает нормально")

    @dp.message(F.text)
    async def handle_message(message: Message):
        """Обработка текстовых сообщений"""
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        
        # Анализируем эмоциональный вектор
        emotion_vector = await analyze_emotion_vector(text)
        
        # Обрабатываем сообщение
        await process_message(user_id, text, emotion_vector, chat_id, bot)
