import json
import re
import random
from typing import Dict, List


class MoralSchemaExtractor:
    def __init__(self):
        self.emotions_list = [
            "Trusting", "Kind-hearted", "Enthusiastic", "Respectful", "Supportive",
            "Confident", "Responsible", "Bold", "Open", "Eager to learn",
            "Sincere", "Encouraging", "Vulnerable", "Praiseworthy", "Goal-oriented",
            "Inspiring", "Mocking", "Disrespectful", "Distrustful", "Confrontational",
            "Unkind", "Insecure", "Serious", "Amused", "Resilient", "Determined",
            "Loyal", "Competitive", "Humble", "Prideful", "Empathetic", "Indifferent",
            "Curious", "Defensive", "Cooperative", "Playful", "Cautious", "Friendly",
            "Grateful", "Indebted", "Dutiful", "Expectant", "Benevolent", 
            "Slightly Superior", "Patient", "Suspicious", "Pragmatic", "Admiring",
            "Hesitant", "Unaware", "Neutral", "Inspired", "Flattered", "Surprised",
            "Protective", "Nurturing", "Dependent", "Secure", "Obedient", "Driven",
            "Focused"
        ]
    
    async def extract_schemas_from_text(self, text: str, source: str = "Unknown") -> List[Dict]:
        from utils.gpt_client import gpt_request
        
        system_prompt = f"""Ты эксперт по межличностным отношениям.

Найди МОРАЛЬНЫЕ СХЕМЫ в тексте.

Эмоции: {', '.join(self.emotions_list)}

Верни валидный JSON:
[
  {{
    "name": "Название",
    "description": "Описание",
    "participant_roles": ["role_a", "role_b"],
    "conditions": {{
      "role_a_to_role_b": [["Emotion1", 20]],
      "role_b_to_role_a": [["Emotion2", 20]]
    }},
    "target_state": {{
      "role_a": {{"Emotion1": 30}},
      "role_b": {{"Emotion2": 30}}
    }},
    "actions": {{
      "action1": {{
        "description": "Описание",
        "author_delta": {{"Emotion1": 10}},
        "target_delta": {{"Emotion2": 10}}
      }}
    }}
  }}
]

ПРАВИЛА:
1. ТОЛЬКО эмоции из списка
2. Короткие описания
3. БЕЗ markdown
4. Валидный JSON"""
        
        prompt = f'Текст: {text[:2500]}\n\nНайди 1-2 схемы.'
        
        response = await gpt_request(prompt, system_prompt)
        
        if not response:
            return []
        
        try:
            response = response.strip()
            
            # ИСПРАВЛЕНИЕ: правильное использование replace()
            if '```' in response:
                response = response.replace('```json', '').replace('```', '')
            
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start == -1:
                return []
            
            json_str = response[json_start:json_end]
            json_str = json_str.replace('\n', ' ').replace('\r', ' ')
            json_str = json_str.replace('  ', ' ')
            
            schemas = json.loads(json_str)
            
            if not isinstance(schemas, list):
                return []
            
            valid = []
            for s in schemas:
                if all(k in s for k in ['name', 'participant_roles', 'conditions', 'actions']):
                    if s.get('actions') and len(s.get('participant_roles', [])) >= 2:
                        s['schema_key'] = self._generate_key(s['name'])
                        valid.append(s)
            
            if valid:
                print(f"    ✅ Извлечено: {len(valid)}")
            return valid
        
        except Exception as e:
            print(f"    ⚠️  Ошибка: {str(e)[:80]}")
            return []
    
    def _generate_key(self, name: str) -> str:
        if not name:
            return f"schema_{random.randint(1000, 9999)}"
        key = ''
        for char in name.lower():
            if char.isalnum() or char in ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']:
                key += char
            elif char == ' ':
                key += '_'
        return key.strip('_') or f"schema_{random.randint(1000, 9999)}"
    
    def save_schemas_to_file(self, schemas: List[Dict], output_file: str):
        if not schemas:
            code = "MORAL_SCHEMAS = {}\n"
        else:
            code = f"# Схем: {len(schemas)}\n\nMORAL_SCHEMAS = {{\n"
            
            for i, s in enumerate(schemas):
                key = s.get('schema_key', self._generate_key(s.get('name', 'unknown')))
                
                name = str(s.get('name', '')).replace('"', "'")
                desc = str(s.get('description', '')).replace('"', "'")
                
                code += f'    "{key}": {{\n'
                code += f'        "name": "{name}",\n'
                code += f'        "description": "{desc}",\n'
                code += f'        "participant_roles": {json.dumps(s.get("participant_roles", []), ensure_ascii=False)},\n'
                code += f'        "conditions": {json.dumps(s.get("conditions", {}), ensure_ascii=False)},\n'
                code += f'        "target_state": {json.dumps(s.get("target_state", {}), ensure_ascii=False)},\n'
                code += f'        "actions": {{\n'
                
                actions = s.get('actions', {})
                for j, (ak, av) in enumerate(actions.items()):
                    adesc = str(av.get('description', '')).replace('"', "'")
                    code += f'            "{ak}": {{\n'
                    code += f'                "description": "{adesc}",\n'
                    code += f'                "author_delta": {json.dumps(av.get("author_delta", {}), ensure_ascii=False)},\n'
                    code += f'                "target_delta": {json.dumps(av.get("target_delta", {}), ensure_ascii=False)}\n'
                    code += f'            }}'
                    if j < len(actions) - 1:
                        code += ','
                    code += '\n'
                
                code += f'        }}\n    }}'
                if i < len(schemas) - 1:
                    code += ','
                code += '\n'
            
            code += "}\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)