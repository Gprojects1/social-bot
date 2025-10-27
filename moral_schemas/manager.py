import numpy as np
from typing import Dict, List, Optional, Tuple
from aiogram import Bot
import random

from config import AI_AGENT_VIRTUAL_ID, AI_AGENT_REAL_ID
from emotions.models import emotion_model, EMOTIONS, EMOTION_INDEX
from moral_schemas.schemas import MORAL_SCHEMAS
from utils.gpt_client import generate_action_text


class MoralSchemaManager:
    def __init__(self):
        self.active_schemas: Dict[Tuple[int, ...], str] = {}
    
    def get_all_user_pairs(self, virtual_ids: List[int]) -> List[Tuple[int, int]]:
        """Получить все возможные пары пользователей (виртуальные ID)"""
        pairs = []
        
        for i, user1 in enumerate(virtual_ids):
            for user2 in virtual_ids[i+1:]:
                pairs.append((user1, user2))
                pairs.append((user2, user1))
        
        return pairs
    
    def map_participants_to_roles(self, user_pair: Tuple[int, int], schema: dict) -> Optional[Dict[str, int]]:
        """Сопоставить реальных пользователей с ролями в схеме"""
        roles = schema["participant_roles"]
        
        if len(roles) == 2 and len(user_pair) == 2:
            return {roles[0]: user_pair[0], roles[1]: user_pair[1]}
        
        return None
    
    def check_schema_conditions(self, schema: dict, participant_map: Dict[str, int]) -> bool:
        """Проверить условия активации схемы (используя виртуальные ID)"""
        conditions = schema["conditions"]
        roles = schema["participant_roles"]

        print(f"\n🔒 [ADMIN] 🔍 Проверка условий схемы '{schema['name']}'")
        print(f"🔒 [ADMIN] Участники (виртуальные ID): {participant_map}")

        for condition_key, required_emotions in conditions.items():
            from_role = None
            to_role = None
            
            for role in roles:
                if condition_key.startswith(role + "_to_"):
                    from_role = role
                    to_role_part = condition_key[len(role) + 4:]
                    
                    for r in roles:
                        if to_role_part == r or to_role_part.startswith(r):
                            to_role = r
                            break
                    break
            
            if not from_role or not to_role:
                print(f"🔒 [ADMIN]   ⚠️ Не удалось распарсить условие: {condition_key}")
                return False
            
            if from_role not in participant_map or to_role not in participant_map:
                print(f"🔒 [ADMIN]   ⚠️ Роли не найдены: {from_role}, {to_role}")
                return False
            
            from_virtual_id = participant_map[from_role]
            to_virtual_id = participant_map[to_role]
            
            from_rel = emotion_model.get_relation(from_virtual_id, to_virtual_id)
            
            print(f"🔒 [ADMIN]   Проверка: {from_role}(v{from_virtual_id}) → {to_role}(v{to_virtual_id})")
            
            for emotion_name, threshold in required_emotions:
                if emotion_name not in EMOTION_INDEX:
                    print(f"🔒 [ADMIN]     ⚠️ Эмоция '{emotion_name}' отсутствует!")
                    return False
                
                idx = EMOTION_INDEX[emotion_name]
                current_value = from_rel[idx]
                
                if threshold < 0:
                    if current_value > threshold:
                        print(f"🔒 [ADMIN]     ❌ {emotion_name}: {current_value:.1f} > {threshold}")
                        return False
                    print(f"🔒 [ADMIN]     ✅ {emotion_name}: {current_value:.1f} <= {threshold}")
                else:
                    if current_value < threshold:
                        print(f"🔒 [ADMIN]     ❌ {emotion_name}: {current_value:.1f} < {threshold}")
                        return False
                    print(f"🔒 [ADMIN]     ✅ {emotion_name}: {current_value:.1f} >= {threshold}")
        
        print(f"🔒 [ADMIN] ✅ ВСЕ условия выполнены!")
        return True
    
    def select_best_action(self, schema: dict, participant_map: Dict[str, int]) -> Optional[str]:
        """Выбрать лучшее действие"""
        actions = schema["actions"]
        target_state = schema.get("target_state", {})
        
        if not target_state:
            return random.choice(list(actions.keys()))
        
        roles = list(participant_map.keys())
        author_role = roles[0]
        target_role = roles[1] if len(roles) > 1 else roles[0]
        
        author_id = participant_map[author_role]
        target_id = participant_map[target_role]
        
        best_action = None
        best_impact = -1
        
        for action_key, action in actions.items():
            impact = self._calculate_action_impact(
                action, author_id, target_id, target_state, author_role, target_role
            )
            
            if impact > best_impact:
                best_impact = impact
                best_action = action_key
        
        if best_action is None:
            best_action = random.choice(list(actions.keys()))
        
        return best_action
    
    def _calculate_action_impact(self, action: dict, author_id: int, target_id: int,
                                 target_state: dict, author_role: str, target_role: str) -> float:
        """Рассчитать влияние действия на целевое состояние"""
        author_delta = action.get("author_delta", {})
        target_delta = action.get("target_delta", {})
        
        impact = 0
        
        if author_role in target_state:
            current_rel = emotion_model.get_relation(author_id, target_id)
            target_emotions = target_state[author_role]
            
            for emotion, target_value in target_emotions.items():
                if emotion in EMOTION_INDEX and emotion in author_delta:
                    idx = EMOTION_INDEX[emotion]
                    current_value = current_rel[idx]
                    new_value = current_value + author_delta[emotion]
                    
                    old_distance = abs(target_value - current_value)
                    new_distance = abs(target_value - new_value)
                    
                    if new_distance < old_distance:
                        impact += (old_distance - new_distance)
        
        if target_role in target_state:
            current_rel = emotion_model.get_relation(target_id, author_id)
            target_emotions = target_state[target_role]
            
            for emotion, target_value in target_emotions.items():
                if emotion in EMOTION_INDEX and emotion in target_delta:
                    idx = EMOTION_INDEX[emotion]
                    current_value = current_rel[idx]
                    new_value = current_value + target_delta[emotion]
                    
                    old_distance = abs(target_value - current_value)
                    new_distance = abs(target_value - new_value)
                    
                    if new_distance < old_distance:
                        impact += (old_distance - new_distance)
        
        return max(impact, 0)
    
    async def execute_schema_action(self, schema_key: str, participant_map: Dict[str, int],
                                   action_key: str, all_participants: List[Dict], bot: Bot) -> bool:
        """Выполнить действие схемы и отправить в виртуальный чат"""
        schema = MORAL_SCHEMAS[schema_key]
        action = schema["actions"][action_key]
        
        roles = list(participant_map.keys())
        author_role = roles[0]
        target_role = roles[1] if len(roles) > 1 else roles[0]
        
        author_virtual_id = participant_map[author_role]
        target_virtual_id = participant_map[target_role]
        
        # ЕСЛИ АГЕНТ УЧАСТНИК СХЕМЫ - ГЕНЕРИРУЕМ СООБЩЕНИЕ
        if author_virtual_id == AI_AGENT_VIRTUAL_ID:
            print(f"🔒 [ADMIN] 🤖 Агент (v{AI_AGENT_VIRTUAL_ID}) участник схемы - генерирую сообщение")
            
            context = f"Схема '{schema['name']}': {schema['description']}"
            action_text = await generate_action_text(
                action_key,
                action["description"],
                context
            )
            
            if action_text:
                # Отправляем сообщение от имени агента во все личные чаты
                message_text = f"💬 [ID {AI_AGENT_VIRTUAL_ID}]: {action_text}"
                
                for participant in all_participants:
                    if participant["virtual_id"] != AI_AGENT_VIRTUAL_ID:
                        try:
                            await bot.send_message(participant["telegram_id"], message_text)
                        except Exception as e:
                            print(f"🔒 [ADMIN] Ошибка отправки участнику {participant['telegram_id']}: {e}")
                
                print(f"🔒 [ADMIN] ✅ Агент выполнил '{action_key}': {action_text[:50]}...")
        else:
            print(f"🔒 [ADMIN] 👥 Схема между людьми - только логирование")
        
        # Применяем эффекты (используем виртуальные ID)
        self._apply_action_effects(author_virtual_id, target_virtual_id, action)
        
        # Запоминаем схему
        schema_key_tuple = tuple(sorted([author_virtual_id, target_virtual_id]))
        self.active_schemas[schema_key_tuple] = schema_key
        
        return True
    
    def _apply_action_effects(self, author_virtual_id: int, target_virtual_id: int, action: dict):
        """Применить эффекты действия (используя виртуальные ID)"""
        author_delta = action.get("author_delta", {})
        target_delta = action.get("target_delta", {})
        
        if author_delta:
            delta_vector = np.zeros(len(EMOTIONS))
            for emotion, value in author_delta.items():
                if emotion in EMOTION_INDEX:
                    delta_vector[EMOTION_INDEX[emotion]] = value
            emotion_model.update_relation(author_virtual_id, target_virtual_id, delta_vector.tolist())
        
        if target_delta:
            delta_vector = np.zeros(len(EMOTIONS))
            for emotion, value in target_delta.items():
                if emotion in EMOTION_INDEX:
                    delta_vector[EMOTION_INDEX[emotion]] = value
            emotion_model.update_relation(target_virtual_id, author_virtual_id, delta_vector.tolist())
    
    async def check_and_activate_schemas(self, virtual_ids: List[int], 
                                        all_participants: List[Dict], bot: Bot) -> bool:
        """Проверить и активировать схемы (используя виртуальные ID)
        
        Returns:
            bool: True если хотя бы одна схема активирована
        """
        print(f"🔒 [ADMIN] Проверка схем для виртуальных ID: {virtual_ids}")
        
        user_pairs = self.get_all_user_pairs(virtual_ids)
        
        schemas_by_priority = sorted(
            MORAL_SCHEMAS.items(),
            key=lambda x: x[1].get("priority", 0),
            reverse=True
        )
        
        for schema_key, schema in schemas_by_priority:
            for user_pair in user_pairs:
                participant_map = self.map_participants_to_roles(user_pair, schema)
                if not participant_map:
                    continue
                
                if self.check_schema_conditions(schema, participant_map):
                    print(f"🔒 [ADMIN] ✅ Схема '{schema['name']}' активирована для виртуальных ID {user_pair}!")
                    
                    best_action = self.select_best_action(schema, participant_map)
                    if best_action:
                        await self.execute_schema_action(schema_key, participant_map, best_action, 
                                                        all_participants, bot)
                        return True
        
        return False
    
    def print_active_schemas_report(self):
        """Вывести отчет об активных схемах"""
        print("\n" + "="*70)
        print("📋 АКТИВНЫЕ МОРАЛЬНЫЕ СХЕМЫ")
        print("="*70)
        
        if not self.active_schemas:
            print("Нет активных схем")
            return
        
        for (user1, user2), schema_key in self.active_schemas.items():
            schema = MORAL_SCHEMAS.get(schema_key, {})
            print(f"\nСхема: {schema.get('name', schema_key)}")
            print(f"Участники (виртуальные ID): {user1} ↔ {user2}")
            print(f"Описание: {schema.get('description', 'Нет описания')}")
        
        print("="*70 + "\n")
