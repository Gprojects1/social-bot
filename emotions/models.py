import numpy as np
from typing import Dict, Tuple, List

EMOTIONS = [
    "Trusting", "Kind-hearted", "Enthusiastic", "Respectful", "Supportive",
    "Confident", "Responsible", "Bold", "Open", "Eager to learn",
    "Sincere", "Encouraging", "Vulnerable", "Praiseworthy", "Goal-oriented",
    "Inspiring", "Mocking", "Disrespectful", "Distrustful", "Confrontational",
    "Unkind", "Insecure", "Serious", "Amused", "Resilient", "Determined",
    "Loyal", "Competitive", "Humble", "Prideful", "Empathetic", "Indifferent",
    "Curious", "Defensive", "Cooperative", "Playful", "Cautious", "Friendly"
]

EMOTION_INDEX = {emotion: i for i, emotion in enumerate(EMOTIONS)}

class EmotionModel:
    def __init__(self):
        self.relations: Dict[Tuple[int, int], np.ndarray] = {}
    
    def get_relation(self, from_id: int, to_id: int) -> np.ndarray:
        """Получить вектор отношений"""
        key = (from_id, to_id)
        if key not in self.relations:
            self.relations[key] = np.zeros(len(EMOTIONS))
        return self.relations[key]
    
    def update_relation(self, from_id: int, to_id: int, delta: list) -> np.ndarray:
        """Обновить вектор отношений"""
        rel = self.get_relation(from_id, to_id)
        delta_array = np.array(delta)
        rel += delta_array
        self.relations[(from_id, to_id)] = rel
        return rel
    
    def reset_relations(self, user_id: int):
        """Сбросить отношения для пользователя"""
        keys_to_remove = []
        for (from_id, to_id) in self.relations.keys():
            if from_id == user_id or to_id == user_id:
                keys_to_remove.append((from_id, to_id))
        
        for key in keys_to_remove:
            self.relations.pop(key, None)
    
    def get_all_relations_for_user(self, user_id: int) -> List[tuple]:
        """Получить все отношения, связанные с пользователем"""
        user_relations = []
        for (from_id, to_id), vector in self.relations.items():
            if from_id == user_id or to_id == user_id:
                user_relations.append((from_id, to_id, vector))
        return user_relations
    
    def get_relation_strength(self, from_id: int, to_id: int) -> float:
        """Получить общую силу отношений (норма вектора)"""
        rel = self.get_relation(from_id, to_id)
        return np.linalg.norm(rel)
    
    def print_relations_report(self):
        """Напечатать полный отчет об отношениях для админа"""
        print("\n" + "="*50)
        print("🔒 [ADMIN] ПОЛНЫЙ ОТЧЕТ ОТНОШЕНИЙ")
        print("="*50)
        
        if not self.relations:
            print("🔒 [ADMIN] Пока нет установленных отношений")
            return
        
        for (from_id, to_id), vector in self.relations.items():
            from_name = "🤖 Агент" if from_id == -1 else f"👤 Участник {from_id}"
            to_name = "🤖 Агент" if to_id == -1 else f"👤 Участник {to_id}"
            
            strong_emotions = []
            for i, value in enumerate(vector):
                if abs(value) > 10:  # Показываем только сильные эмоции
                    emotion_name = EMOTIONS[i]
                    strong_emotions.append(f"{emotion_name}: {value:.1f}")
            
            if strong_emotions:
                print(f"{from_name} -> {to_name}:")
                print(f"  {', '.join(strong_emotions)}")
            else:
                print(f"{from_name} -> {to_name}: (нейтральные)")
        
        print("="*50)

# Глобальный экземпляр модели эмоций
emotion_model = EmotionModel()