import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import numpy as np

from config import AI_AGENT_VIRTUAL_ID, AI_AGENT_REAL_ID, ADMIN_ID
from emotions.models import emotion_model, EMOTIONS, EMOTION_INDEX
from emotions.analyzer import analyze_emotion_vector
from moral_schemas.manager import MoralSchemaManager
from utils.gpt_client import gpt_request
from database.chat_db import chat_db
from emotions.analyzer import analyze_emotions_per_target

def extract_virtual_ids(text: str) -> list[int]:
    """Извлечь виртуальные ID из текста сообщения"""
    patterns = [
        r'@id(\d+)',
        r'#id(\d+)',
        r'\bid(\d+)'
    ]
    
    virtual_ids = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            try:
                virtual_id = int(match)
                virtual_ids.append(virtual_id)
            except ValueError:
                continue
    
    return list(set(virtual_ids))


async def generate_simple_response(user_message: str, sender_virtual_id: int) -> str:
    """Генерация простого ответа агента через DeepSeek"""
    system_prompt = """Ты — студент в новом коллективе. 
Говори естественно, без формальностей. Не веди себя вежливо, веди себя нейтрально.
НЕ используй эмодзи, markdown и специальное форматирование.
Отвечай кратко — максимум 1-2 предложения."""
    
    prompt = f"Участник {sender_virtual_id} написал: {user_message}\n\nТвой ответ:"
    
    response = await gpt_request(prompt, system_prompt)
    
    if not response:
        fallbacks = [
            "Понял, интересно.",
            "Хорошо, давай обсудим.",
            "Окей, продолжай.",
        ]
        import random
        return random.choice(fallbacks)
    
    return response.strip()


async def broadcast_message(sender_virtual_id: int, text: str, bot: Bot, exclude_ids: list = None):
    """Разослать сообщение всем участникам виртуального чата"""
    participants = chat_db.get_all_participants()
    
    message_text = f"💬 [ID {sender_virtual_id}]: {text}"
    
    if exclude_ids is None:
        exclude_ids = []
    
    for participant in participants:
        # Не отправляем отправителю
        if participant["virtual_id"] == sender_virtual_id:
            continue
        
        # Не отправляем исключённым
        if participant["virtual_id"] in exclude_ids:
            continue
        
        # Пропускаем агента (он не реальный пользователь в Telegram)
        if participant["virtual_id"] == AI_AGENT_VIRTUAL_ID:
            continue
        
        try:
            await bot.send_message(participant["telegram_id"], message_text)
        except Exception as e:
            print(f"🔒 [ADMIN] Ошибка отправки участнику {participant['telegram_id']}: {e}")


async def process_message(sender_telegram_id: int, text: str, bot: Bot):
    """Обработать сообщение в виртуальном чате"""
    
    # Получаем виртуальный ID отправителя
    sender_virtual_id = chat_db.get_virtual_id(sender_telegram_id)
    
    if not sender_virtual_id:
        print(f"🔒 [ADMIN] Пользователь {sender_telegram_id} не зарегистрирован")
        return
    
    print(f"\n{'='*70}")
    print(f"🔒 [ADMIN] Новое сообщение от Virtual ID {sender_virtual_id} (Telegram {sender_telegram_id})")
    print(f"🔒 [ADMIN] Текст: {text[:100]}...")
    print(f"{'='*70}")
    
    # Извлекаем упоминания (виртуальные ID)
    mentioned_virtual_ids = extract_virtual_ids(text)
    
    print(f"🔒 [ADMIN] 👥 Упоминания (виртуальные ID): {mentioned_virtual_ids if mentioned_virtual_ids else 'НЕТ'}")
    
    # Рассылаем сообщение всем участникам
    await broadcast_message(sender_virtual_id, text, bot)
    
    # Если нет упоминаний - только рассылка, без обновления эмоций
    if not mentioned_virtual_ids:
        print(f"🔒 [ADMIN] ⚠️ Нет адресатов - только рассылка")
        print(f"{'='*70}\n")
        return
    
    # НОВОЕ: Анализируем эмоции контекстно для каждого упомянутого участника
    print(f"🔒 [ADMIN] 🧠 Анализирую эмоции контекстно для каждого участника...")
    emotions_per_target = await analyze_emotions_per_target(text, mentioned_virtual_ids)
    
    # ШАГ 1: ОБНОВЛЯЕМ ЭМОЦИИ (используем виртуальные ID)
    print(f"\n🔒 [ADMIN] === ШАГ 1: ОБНОВЛЕНИЕ ЭМОЦИЙ (КОНТЕКСТНО) ===")
    
    for target_virtual_id in mentioned_virtual_ids:
        # Получаем эмоциональный вектор для конкретного target_id
        emotion_vector = emotions_per_target.get(target_virtual_id, np.zeros(len(EMOTIONS)))
        
        top_emotions = [(EMOTIONS[i], round(emotion_vector[i], 1)) 
                       for i in np.argsort(emotion_vector)[-5:] if emotion_vector[i] > 0]
        
        print(f"🔒 [ADMIN] 🎯 Эмоции к ID {target_virtual_id}: {top_emotions}")
        
        # Обновляем отношение АВТОРА к АДРЕСАТУ
        print(f"🔒 [ADMIN] ⬆️ Обновление: Virtual ID {sender_virtual_id} → Virtual ID {target_virtual_id} (коэф. 1.0)")
        emotion_model.update_relation(sender_virtual_id, target_virtual_id, emotion_vector.tolist())
        
        current_rel = emotion_model.get_relation(sender_virtual_id, target_virtual_id)
        top_rel = [(EMOTIONS[i], round(current_rel[i], 1)) 
                  for i in np.argsort(current_rel)[-5:] if current_rel[i] > 0]
        print(f"🔒 [ADMIN] 📊 Эмоции Virtual ID {sender_virtual_id} → Virtual ID {target_virtual_id}: {top_rel}")
        
        # Обновляем отношение АДРЕСАТА к АВТОРУ (зеркальная реакция)
        mirrored_emotion_vector = emotion_vector * 0.5
        print(f"🔒 [ADMIN] ⬆️ Обновление (зеркало): Virtual ID {target_virtual_id} → Virtual ID {sender_virtual_id} (коэф. 0.5)")
        emotion_model.update_relation(target_virtual_id, sender_virtual_id, mirrored_emotion_vector.tolist())
        
        mirrored_rel = emotion_model.get_relation(target_virtual_id, sender_virtual_id)
        top_mirrored = [(EMOTIONS[i], round(mirrored_rel[i], 1)) 
                       for i in np.argsort(mirrored_rel)[-5:] if mirrored_rel[i] > 0]
        print(f"🔒 [ADMIN] 📊 Эмоции Virtual ID {target_virtual_id} → Virtual ID {sender_virtual_id}: {top_mirrored}")
    
    # ШАГ 2: ПРОВЕРЯЕМ МОРАЛЬНЫЕ СХЕМЫ
    print(f"\n🔒 [ADMIN] === ШАГ 2: ПРОВЕРКА МОРАЛЬНЫХ СХЕМ ===")
    
    schema_manager = MoralSchemaManager()
    all_involved_virtual_ids = [sender_virtual_id] + mentioned_virtual_ids
    all_participants = chat_db.get_all_participants()
    
    schema_activated = await schema_manager.check_and_activate_schemas(
        all_involved_virtual_ids, all_participants, bot
    )
    
    # ШАГ 3: ЕСЛИ СХЕМА НЕ СРАБОТАЛА, НО ОБРАЩЕНИЕ К АГЕНТУ - ПРОСТОЙ ОТВЕТ
    if not schema_activated and AI_AGENT_VIRTUAL_ID in mentioned_virtual_ids:
        print(f"\n🔒 [ADMIN] === ШАГ 3: ГЕНЕРАЦИЯ ПРОСТОГО ОТВЕТА АГЕНТА ===")
        print(f"🔒 [ADMIN] 💬 Схемы не активированы, но есть обращение к агенту (ID {AI_AGENT_VIRTUAL_ID})")
        print(f"🔒 [ADMIN] 🤖 Генерирую ответ через DeepSeek...")
        
        response_text = await generate_simple_response(text, sender_virtual_id)
        
        if response_text:
            # Отправляем ответ всем участникам (как обычное сообщение в чате)
            await broadcast_message(AI_AGENT_VIRTUAL_ID, response_text, bot)
            print(f"🔒 [ADMIN] ✅ Агент ответил: {response_text[:50]}...")
            
            # Анализируем эмоции ответа агента
            response_emotion_vector = await analyze_emotion_vector(response_text)
            
            # Обновляем отношение АГЕНТА к ПОЛЬЗОВАТЕЛЮ
            print(f"🔒 [ADMIN] ⬆️ Обновление после ответа: Virtual ID {AI_AGENT_VIRTUAL_ID} → Virtual ID {sender_virtual_id} (коэф. 1.0)")
            emotion_model.update_relation(AI_AGENT_VIRTUAL_ID, sender_virtual_id, response_emotion_vector.tolist())
            
            updated_rel = emotion_model.get_relation(AI_AGENT_VIRTUAL_ID, sender_virtual_id)
            top_updated = [(EMOTIONS[i], round(updated_rel[i], 1)) 
                          for i in np.argsort(updated_rel)[-5:] if updated_rel[i] > 0]
            print(f"🔒 [ADMIN] 📊 Эмоции Virtual ID {AI_AGENT_VIRTUAL_ID} → Virtual ID {sender_virtual_id}: {top_updated}")
            
            # Обновляем отношение ПОЛЬЗОВАТЕЛЯ к АГЕНТУ (реакция на ответ)
            mirrored_response = response_emotion_vector * 0.5
            print(f"🔒 [ADMIN] ⬆️ Обновление (реакция на ответ): Virtual ID {sender_virtual_id} → Virtual ID {AI_AGENT_VIRTUAL_ID} (коэф. 0.5)")
            emotion_model.update_relation(sender_virtual_id, AI_AGENT_VIRTUAL_ID, mirrored_response.tolist())
            
            user_to_ai = emotion_model.get_relation(sender_virtual_id, AI_AGENT_VIRTUAL_ID)
            top_user_to_ai = [(EMOTIONS[i], round(user_to_ai[i], 1)) 
                             for i in np.argsort(user_to_ai)[-5:] if user_to_ai[i] > 0]
            print(f"🔒 [ADMIN] 📊 Эмоции Virtual ID {sender_virtual_id} → Virtual ID {AI_AGENT_VIRTUAL_ID}: {top_user_to_ai}")
    
    print(f"🔒 [ADMIN] === КОНЕЦ ОБРАБОТКИ ===\n")



async def setup_handlers(dp: Dispatcher, bot: Bot):
    """Настройка обработчиков сообщений"""
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        
        # Регистрируем участника
        virtual_id = chat_db.register_participant(user_id, username)
        
        # Получаем список всех участников
        participants = chat_db.get_all_participants()
        participant_list = "\n".join([
            f"  • ID {p['virtual_id']}"
            for p in participants
        ])
        
        await message.answer(
            f"👋 Добро пожаловать в виртуальный чат!\n\n"
            f"🆔 Ваш ID: {virtual_id}\n\n"
            f"👥 Участники чата:\n{participant_list}\n\n"
            f"💡 Чтобы обратиться к кому-то, используйте @id в сообщении\n"
            f"Пример: @id3 привет!\n\n"
            f"📝 Все ваши сообщения будут видны всем участникам чата.\n\n"
            f"Команды:\n"
            f"/help - справка\n"
            f"/participants - список участников"
        )
    
    @dp.message(Command("help"))
    async def cmd_help(message: Message):
        user_id = message.from_user.id
        virtual_id = chat_db.get_virtual_id(user_id)
        
        if not virtual_id:
            await message.answer("⚠️ Сначала используйте /start")
            return
        
        await message.answer(
            f"ℹ️ Как пользоваться виртуальным чатом:\n\n"
            f"1. Пишите сообщения — они видны всем\n"
            f"2. Упоминайте участников: @id3\n"
            f"3. Без упоминаний сообщение тоже отправляется всем\n\n"
            f"Примеры:\n"
            f"• Привет всем! (видят все)\n"
            f"• @id3 как дела? (видят все, но обращение к ID 3)\n\n"
            f"Команды:\n"
            f"/participants - список участников\n"
            f"/start - перезапуск"
        )
    
    @dp.message(Command("participants"))
    async def cmd_participants(message: Message):
        user_id = message.from_user.id
        
        if not chat_db.is_participant(user_id):
            await message.answer("⚠️ Сначала используйте /start")
            return
        
        participants = chat_db.get_all_participants()
        participant_list = "\n".join([
            f"  • ID {p['virtual_id']}"
            for p in participants
        ])
        
        await message.answer(
            f"👥 Участники виртуального чата:\n{participant_list}\n\n"
            f"Используйте @id для обращения к участнику"
        )
    
    @dp.message(F.text)
    async def handle_message(message: Message):
        """Обработка текстовых сообщений"""
        user_id = message.from_user.id
        text = message.text
        
        # Проверяем регистрацию
        if not chat_db.is_participant(user_id):
            await message.answer("⚠️ Сначала используйте /start для входа в чат")
            return
        
        # Обрабатываем сообщение
        await process_message(user_id, text, bot)
