import numpy as np
import json
from typing import Optional
from utils.gpt_client import gpt_request
from .models import EMOTIONS, EMOTION_INDEX

async def analyze_emotion_vector(message_text: str) -> np.ndarray:
    """Анализ эмоционального вектора сообщения"""
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
        # Возвращаем базовый вектор для нейтрального сообщения
        vector = np.zeros(len(EMOTIONS))
        vector[EMOTION_INDEX["Open"]] = 10
        vector[EMOTION_INDEX["Respectful"]] = 5
        return vector
    
    try:
        # Извлекаем JSON из ответа
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