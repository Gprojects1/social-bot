import json
import os
from typing import Optional, List, Dict

class ChatDatabase:
    """База данных виртуального чата"""
    
    def __init__(self, db_file: str = "chat_data.json"):
        self.db_file = db_file
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """Загрузить данные из файла"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "participants": {},  # {real_telegram_id: virtual_id}
            "virtual_to_real": {},  # {virtual_id: real_telegram_id}
            "next_virtual_id": 1
        }
    
    def _save_data(self):
        """Сохранить данные в файл"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def register_participant(self, telegram_id: int, username: str = None) -> int:
        """Зарегистрировать участника и выдать виртуальный ID"""
        telegram_id_str = str(telegram_id)
        
        if telegram_id_str in self.data["participants"]:
            return self.data["participants"][telegram_id_str]
        
        virtual_id = self.data["next_virtual_id"]
        self.data["participants"][telegram_id_str] = virtual_id
        self.data["virtual_to_real"][str(virtual_id)] = {
            "telegram_id": telegram_id,
            "username": username
        }
        self.data["next_virtual_id"] += 1
        self._save_data()
        
        return virtual_id
    
    def get_virtual_id(self, telegram_id: int) -> Optional[int]:
        """Получить виртуальный ID по реальному Telegram ID"""
        return self.data["participants"].get(str(telegram_id))
    
    def get_real_id(self, virtual_id: int) -> Optional[int]:
        """Получить реальный Telegram ID по виртуальному ID"""
        user_data = self.data["virtual_to_real"].get(str(virtual_id))
        return user_data["telegram_id"] if user_data else None
    
    def get_all_participants(self) -> List[Dict]:
        """Получить список всех участников"""
        participants = []
        for virtual_id_str, user_data in self.data["virtual_to_real"].items():
            participants.append({
                "virtual_id": int(virtual_id_str),
                "telegram_id": user_data["telegram_id"],
                "username": user_data.get("username", "Unknown")
            })
        return participants
    
    def is_participant(self, telegram_id: int) -> bool:
        """Проверить, является ли пользователь участником"""
        return str(telegram_id) in self.data["participants"]


# Глобальный экземпляр БД
chat_db = ChatDatabase()
