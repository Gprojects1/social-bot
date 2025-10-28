import numpy as np
import json
from typing import Optional, Dict, List
from utils.gpt_client import gpt_request
from .models import EMOTIONS, EMOTION_INDEX


async def analyze_emotion_vector(message_text: str) -> np.ndarray:
    """Анализ эмоционального вектора сообщения (общий)"""
    system_prompt = f"""Ты эксперт по анализу эмоций. 
Твоя задача - разложить текст сообщения по вектору эмоций.
Доступные эмоции: {', '.join(EMOTIONS)}
Верни ТОЛЬКО JSON в формате: {{"emotion_name": value}}, где value от -30 до 30.
Положительные значения означают наличие эмоции, отрицательные - противоположную эмоцию.
НЕ добавляй никаких комментариев, только JSON."""
    
    prompt = f'Проанализируй эмоции в сообщении: "{message_text}"'
    
    response = await gpt_request(prompt, system_prompt)
    
    if not response:
        print("GPT не вернул ответ, используем базовые эмоции")
        vector = np.zeros(len(EMOTIONS))
        vector[EMOTION_INDEX["Open"]] = 10
        vector[EMOTION_INDEX["Respectful"]] = 5
        return vector
    
    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        
        if json_start == -1 or json_end <= json_start:
            print(f"JSON не найден в ответе: {response}")
            return np.zeros(len(EMOTIONS))
        
        json_str = response[json_start:json_end]
        emotion_dict = json.loads(json_str)
        
        vector = np.zeros(len(EMOTIONS))
        for emotion, value in emotion_dict.items():
            if emotion in EMOTION_INDEX:
                vector[EMOTION_INDEX[emotion]] = float(value)
        
        print(f"Parsed emotion vector: {dict(zip(EMOTIONS, vector))}")
        return vector
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response was: {response}")
    except Exception as e:
        print(f"Error parsing emotion vector: {type(e).__name__}: {e}")
    
    return np.zeros(len(EMOTIONS))


async def analyze_emotions_per_target(message_text: str, mentioned_ids: List[int]) -> Dict[int, np.ndarray]:
    """
    Анализ эмоций отдельно для каждого упомянутого участника
    
    Args:
        message_text: Полный текст сообщения
        mentioned_ids: Список виртуальных ID упомянутых участников
    
    Returns:
        Словарь {target_id: emotion_vector}
    """
    if not mentioned_ids:
        return {}
    
    # Более подробный system prompt
    system_prompt = f"""Ты эксперт по анализу эмоций в сообщениях.
Проанализируй сообщение и определи эмоциональное отношение автора к КАЖДОМУ упомянутому участнику.

Доступные эмоции: {', '.join(EMOTIONS)}

ВАЖНО: Даже если отношение негативное, ты ОБЯЗАН указать эмоции!

Верни ТОЛЬКО JSON в формате:
{{
  "id_number": {{"Emotion1": 25, "Emotion2": 30, "Emotion3": 28}},
  "id_number": {{"Emotion4": 20, "Emotion5": 22}}
}}

где ключ - это номер ID (без "id"), а значения - эмоции от -30 до 30.
НЕ добавляй комментариев, пояснений или текста вне JSON!"""
    
    # Создаём более явный запрос
    ids_list = ", ".join([f"ID {id}" for id in mentioned_ids])
    prompt = f"""Сообщение: "{message_text}"

Упомянутые участники: {ids_list}

Проанализируй эмоциональное отношение автора к КАЖДОМУ участнику:
{chr(10).join([f'- ID {id}: какие эмоции испытывает автор?' for id in mentioned_ids])}

Верни JSON с анализом для КАЖДОГО ID."""
    
    print(f"🔒 [DEBUG] Отправляю запрос к GPT для контекстного анализа...")
    response = await gpt_request(prompt, system_prompt)
    
    if not response:
        print("🔒 [DEBUG] GPT не вернул ответ, используем fallback")
        # Fallback: анализируем общие эмоции и применяем ко всем
        general_vector = await analyze_emotion_vector(message_text)
        return {target_id: general_vector.copy() for target_id in mentioned_ids}
    
    print(f"🔒 [DEBUG] Ответ GPT: {response[:500]}")
    
    try:
        # Ищем JSON в ответе
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        
        if json_start == -1 or json_end <= json_start:
            print(f"🔒 [DEBUG] JSON не найден в ответе")
            general_vector = await analyze_emotion_vector(message_text)
            return {target_id: general_vector.copy() for target_id in mentioned_ids}
        
        json_str = response[json_start:json_end]
        print(f"🔒 [DEBUG] Извлечённый JSON: {json_str}")
        
        per_target_dict = json.loads(json_str)
        print(f"🔒 [DEBUG] Распарсенный словарь: {per_target_dict}")
        
        result = {}
        
        for target_id in mentioned_ids:
            # Пробуем множество вариантов ключей
            target_key = None
            possible_keys = [
                str(target_id),           # "1"
                f"id{target_id}",         # "id1"
                f"ID{target_id}",         # "ID1"
                f"@id{target_id}",        # "@id1"
                f"participant_{target_id}", # "participant_1"
                int(target_id) if isinstance(target_id, str) else target_id  # числовой ключ
            ]
            
            for possible_key in possible_keys:
                if possible_key in per_target_dict:
                    target_key = possible_key
                    print(f"🔒 [DEBUG] Найден ключ '{target_key}' для ID {target_id}")
                    break
            
            if target_key and isinstance(per_target_dict[target_key], dict):
                # Создаём вектор эмоций для этого target_id
                vector = np.zeros(len(EMOTIONS))
                emotions_found = 0
                
                for emotion, value in per_target_dict[target_key].items():
                    if emotion in EMOTION_INDEX:
                        vector[EMOTION_INDEX[emotion]] = float(value)
                        emotions_found += 1
                        print(f"🔒 [DEBUG] ID {target_id}: {emotion} = {value}")
                
                if emotions_found > 0:
                    result[target_id] = vector
                    print(f"🔒 [DEBUG] ✅ Для ID {target_id} найдено {emotions_found} эмоций")
                else:
                    print(f"🔒 [DEBUG] ⚠️ Для ID {target_id} не найдено подходящих эмоций, используем общий анализ")
                    result[target_id] = await analyze_emotion_vector(message_text)
            else:
                print(f"🔒 [DEBUG] ❌ Не найдены эмоции для ID {target_id} (ключ не найден), используем общий анализ")
                result[target_id] = await analyze_emotion_vector(message_text)
        
        # ВАЖНО: Проверяем, что для всех ID есть результаты
        for target_id in mentioned_ids:
            if target_id not in result:
                print(f"🔒 [DEBUG] ⚠️ ID {target_id} отсутствует в результатах, добавляем общий анализ")
                result[target_id] = await analyze_emotion_vector(message_text)
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"🔒 [DEBUG] Error parsing JSON: {e}")
        print(f"🔒 [DEBUG] Response was: {response}")
    except Exception as e:
        print(f"🔒 [DEBUG] Error in contextual analysis: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    # Финальный fallback
    print(f"🔒 [DEBUG] Используем финальный fallback - общий анализ для всех")
    general_vector = await analyze_emotion_vector(message_text)
    return {target_id: general_vector.copy() for target_id in mentioned_ids}
