MORAL_SCHEMAS = {
    "comradeship": {
        "name": "Приятельство",
        "description": "Симметричные дружеские отношения",
        "participant_roles": ["participant_a", "participant_b"],
        "conditions": {
            "participant_a_to_participant_b": [("Trusting", 20), ("Friendly", 20), ("Enthusiastic", 15)],
            "participant_b_to_participant_a": [("Trusting", 20), ("Friendly", 20), ("Enthusiastic", 15)]
        },
        "target_state": {
            "participant_a": {"Trusting": 30, "Friendly": 35, "Supportive": 25, "Enthusiastic": 25},
            "participant_b": {"Trusting": 30, "Friendly": 35, "Supportive": 25, "Enthusiastic": 25}
        },
        "actions": {
            "share_joke": {
                "description": "Поделиться шуткой",
                "author_delta": {"Friendly": 12, "Enthusiastic": 8},
                "target_delta": {"Friendly": 10, "Enthusiastic": 8}
            },
            "support_idea": {
                "description": "Поддержать идею",
                "author_delta": {"Supportive": 10, "Trusting": 8},
                "target_delta": {"Trusting": 10, "Supportive": 8}
            },
            "show_enthusiasm": {
                "description": "Проявить энтузиазм в общении",
                "author_delta": {"Enthusiastic": 10, "Friendly": 8},
                "target_delta": {"Enthusiastic": 8, "Friendly": 8}
            }
        }
    },

    "passive_rivalry": {
        "name": "Незримое соперничество",
        "description": "Конкурентные отношения с взаимным неуважением",
        "participant_roles": ["rival_a", "rival_b"],
        "conditions": {
            "rival_a_to_rival_b": [("Competitive", 15), ("Determined", 15), ("Disrespectful", 10)],
            "rival_b_to_rival_a": [("Competitive", 15), ("Determined", 15), ("Disrespectful", 10)]
        },
        "target_state": {
            "rival_a": {"Competitive": 25, "Determined": 25, "Confident": 20, "Disrespectful": 15},
            "rival_b": {"Competitive": 25, "Determined": 25, "Confident": 20, "Disrespectful": 15}
        },
        "actions": {
            "constructive_challenge": {
                "description": "Нетактично оспорить, оскорбить",
                "author_delta": {"Competitive": 10, "Determined": 8, "Confident": 6},
                "target_delta": {"Determined": 10, "Competitive": 8, "Disrespectful": 5}
            },
            "competitive_demonstration": {
                "description": "Продемонстрировать компетентность",
                "author_delta": {"Confident": 8, "Competitive": 8},
                "target_delta": {"Competitive": 8, "Determined": 6}
            },
            "respectful_acknowledgment": {
                "description": "Признать достижения соперника",
                "author_delta": {"Disrespectful": 6, "Confident": 5},
                "target_delta": {"Disrespectful": 6, "Confident": 5}
            }
        }
    },
    
    "mentorship": {
        "name": "Наставник-Ученик",
        "description": "Асимметричные отношения наставничества",
        "participant_roles": ["mentor", "mentee"],
        "conditions": {
            "mentee_to_mentor": [("Respectful", 20), ("Eager to learn", 15), ("Trusting", 15)],
            "mentor_to_mentee": [("Responsible", 20), ("Supportive", 20), ("Inspiring", 10)]
        },
        "target_state": {
            "mentee": {"Eager to learn": 30, "Confident": 25, "Respectful": 25, "Trusting": 30},
            "mentor": {"Responsible": 30, "Supportive": 30, "Praiseworthy": 20, "Inspiring": 20}
        },
        "actions": {
            "ask_advice": {
                "description": "Спросить совета (ученик)",
                "author_delta": {"Respectful": 10, "Eager to learn": 10, "Trusting": 8},
                "target_delta": {"Responsible": 10, "Supportive": 10}
            },
            "acknowledge_expertise": {
                "description": "Признать опыт (ученик)",
                "author_delta": {"Respectful": 10, "Trusting": 10},
                "target_delta": {"Praiseworthy": 8, "Inspiring": 6}
            },
            "give_guidance": {
                "description": "Дать руководство (наставник)",
                "author_delta": {"Responsible": 12, "Supportive": 12, "Inspiring": 8},
                "target_delta": {"Trusting": 12, "Confident": 10, "Eager to learn": 8}
            },
            "encourage_growth": {
                "description": "Поощрить развитие (наставник)",
                "author_delta": {"Supportive": 10, "Inspiring": 8},
                "target_delta": {"Confident": 10, "Eager to learn": 10}
            }
        }
    },
    
    "joint_mockery": {
        "name": "Совместное высмеивание",
        "description": "Связь через общий юмор над третьим объектом",
        "participant_roles": ["initiator", "participant"],
        "conditions": {
            "initiator_to_participant": [("Amused", 15), ("Playful", 15), ("Supportive", 10)],
            "participant_to_initiator": [("Amused", 15), ("Friendly", 15)]
        },
        "target_state": {
            "initiator": {"Amused": 30, "Supportive": 25, "Friendly": 20, "Playful": 25},
            "participant": {"Amused": 30, "Supportive": 25, "Friendly": 20, "Playful": 20}
        },
        "actions": {
            "initiate_mockery": {
                "description": "Начать высмеивание третьего объекта",
                "author_delta": {"Amused": 10, "Playful": 10},
                "target_delta": {"Amused": 8, "Friendly": 6}
            },
            "join_mockery": {
                "description": "Присоединиться к высмеиванию",
                "author_delta": {"Amused": 12, "Supportive": 10, "Playful": 8},
                "target_delta": {"Amused": 10, "Supportive": 10, "Friendly": 6}
            },
            "build_connection": {
                "description": "Укрепить связь через юмор",
                "author_delta": {"Friendly": 8, "Supportive": 8},
                "target_delta": {"Friendly": 8, "Supportive": 8}
            }
        }
    },
    
    "direct_mockery": {
        "name": "Прямое высмеивание",
        "description": "Агрессивное высмеивание с доминированием",
        "participant_roles": ["mocker", "victim"],
        "conditions": {
            "mocker_to_victim": [("Mocking", 25), ("Disrespectful", 20), ("Prideful", 15)],
            "victim_to_mocker": [("Serious", 20), ("Confrontational", 15), ("Insecure", 10)]
        },
        "target_state": {
            "mocker": {"Mocking": 30, "Disrespectful": 25, "Prideful": 20, "Confident": 20},
            "victim": {"Serious": 30, "Insecure": 25, "Confrontational": 25, "Disrespectful": 15}
        },
        "actions": {
            "direct_insult": {
                "description": "Прямое оскорбление (агрессор)",
                "author_delta": {"Mocking": 12, "Disrespectful": 10, "Prideful": 8},
                "target_delta": {"Insecure": 10, "Defensive": 10, "Serious": 8}
            },
            "sarcastic_comment": {
                "description": "Саркастическое замечание (агрессор)",
                "author_delta": {"Mocking": 10, "Disrespectful": 10, "Confident": 6},
                "target_delta": {"Serious": 8, "Confrontational": 8, "Insecure": 6}
            },
            "defensive_response": {
                "description": "Защитная реакция (жертва)",
                "author_delta": {"Serious": 10, "Confrontational": 10},
                "target_delta": {"Mocking": 5, "Disrespectful": 5}
            },
            "counter_attack": {
                "description": "Ответная атака (жертва)",
                "author_delta": {"Disrespectful": 8, "Confrontational": 8, "Serious": 6},
                "target_delta": {"Mocking": 8, "Disrespectful": 8}
            }
        }
    },
    
    "group_bullying": {
        "name": "Групповая травля",
        "description": "Систематическое подавление одного участника группой",
        "participant_roles": ["aggressor", "victim"],
        "conditions": {
            "aggressor_to_victim": [("Mocking", 25), ("Disrespectful", 20), ("Supportive", -15)],
            "victim_to_aggressor": [("Serious", 25), ("Insecure", 25), ("Defensive", 20)]
        },
        "target_state": {
            "aggressor": {"Mocking": 30, "Disrespectful": 25, "Prideful": 20, "Supportive": -25},
            "victim": {"Insecure": 35, "Serious": 30, "Defensive": 30, "Supportive": -30}
        },
        "actions": {
            "initiate_mobbing": {
                "description": "Создать повод для травли (агрессор)",
                "author_delta": {"Mocking": 12, "Disrespectful": 10, "Prideful": 8},
                "target_delta": {"Insecure": 12, "Serious": 10, "Defensive": 10}
            },
            "public_humiliation": {
                "description": "Публичное унижение (агрессор)",
                "author_delta": {"Mocking": 15, "Disrespectful": 12, "Prideful": 8},
                "target_delta": {"Insecure": 15, "Serious": 12, "Defensive": 10}
            },
            "social_exclusion": {
                "description": "Социальная изоляция (агрессор)",
                "author_delta": {"Supportive": -10, "Disrespectful": 8},
                "target_delta": {"Insecure": 12, "Supportive": -12, "Defensive": 8}
            },
            "defensive_retreat": {
                "description": "Попытка уйти от конфликта (жертва)",
                "author_delta": {"Serious": 10, "Defensive": 12, "Supportive": -8},
                "target_delta": {"Mocking": 3, "Disrespectful": 3}
            },
            "plead_for_mercy": {
                "description": "Попытка урезонить (жертва)",
                "author_delta": {"Insecure": 12, "Defensive": 8},
                "target_delta": {"Mocking": 8, "Disrespectful": 6}
            }
        }
    },
    
    "moral_leadership": {
        "name": "Моральное лидерство",
        "description": "Лидер направляет группу через авторитет и заботу",
        "participant_roles": ["leader", "follower"],
        "conditions": {
            "leader_to_follower": [("Responsible", 25), ("Supportive", 20), ("Inspiring", 15)],
            "follower_to_leader": [("Trusting", 25), ("Respectful", 20), ("Loyal", 15)]
        },
        "target_state": {
            "leader": {"Responsible": 35, "Confident": 30, "Inspiring": 30, "Supportive": 30},
            "follower": {"Trusting": 35, "Respectful": 30, "Loyal": 30, "Confident": 25}
        },
        "actions": {
            "set_shared_goal": {
                "description": "Определить общую цель (лидер)",
                "author_delta": {"Responsible": 12, "Inspiring": 10, "Confident": 10},
                "target_delta": {"Trusting": 12, "Respectful": 8, "Confident": 8}
            },
            "empower_member": {
                "description": "Делегировать ответственность (лидер)",
                "author_delta": {"Supportive": 12, "Responsible": 10, "Inspiring": 8},
                "target_delta": {"Confident": 10, "Trusting": 10, "Loyal": 8}
            },
            "moral_guidance": {
                "description": "Дать моральные ориентиры (лидер)",
                "author_delta": {"Responsible": 10, "Inspiring": 10, "Supportive": 10},
                "target_delta": {"Respectful": 12, "Trusting": 10, "Loyal": 8}
            },
            "defend_leader": {
                "description": "Защитить лидера (последователь)",
                "author_delta": {"Loyal": 12, "Respectful": 10},
                "target_delta": {"Supportive": 10, "Confident": 8}
            },
            "express_loyalty": {
                "description": "Выразить лояльность (последователь)",
                "author_delta": {"Loyal": 10, "Trusting": 10, "Respectful": 8},
                "target_delta": {"Inspiring": 10, "Supportive": 10}
            }
        }
    }
}
