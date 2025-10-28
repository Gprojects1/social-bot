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
    },
    
    "debt_of_gratitude": {
        "name": "Долг благодарности",
        "description": "Асимметричные отношения, где один участник чувствует себя обязанным другому за оказанную помощь или услугу",
        "participant_roles": ["benefactor", "obligated"],
        "conditions": {
            "obligated_to_benefactor": [("Grateful", 20), ("Indebted", 15), ("Respectful", 15)],
            "benefactor_to_obligated": [("Expectant", 15), ("Benevolent", 15), ("Slightly Superior", 10)]
        },
        "target_state": {
            "obligated": {"Grateful": 25, "Indebted": 30, "Respectful": 25, "Dutiful": 20},
            "benefactor": {"Expectant": 25, "Benevolent": 20, "Slightly Superior": 20, "Patient": 15}
        },
        "actions": {
            "remind_of_debt": {
                "description": "Напомнить о долге (благодетель)",
                "author_delta": {"Expectant": 10, "Slightly Superior": 8},
                "target_delta": {"Indebted": 12, "Dutiful": 10}
            },
            "fulfill_obligation": {
                "description": "Выполнить часть долга (обязанный)",
                "author_delta": {"Indebted": -12, "Dutiful": 10, "Grateful": 8},
                "target_delta": {"Benevolent": 10, "Expectant": -8}
            },
            "offer_help": {
                "description": "Предложить помощь (благодетель)",
                "author_delta": {"Benevolent": 12, "Expectant": 8},
                "target_delta": {"Indebted": 15, "Grateful": 10}
            }
        }
    },

    "uneasy_alliance": {
        "name": "Ненадежный союз",
        "description": "Вынужденное сотрудничество между участниками с фундаментальными разногласиями, основанное на общей цели",
        "participant_roles": ["ally_a", "ally_b"],
        "conditions": {
            "ally_a_to_ally_b": [("Cooperative", 15), ("Suspicious", 15), ("Pragmatic", 10)],
            "ally_b_to_ally_a": [("Cooperative", 15), ("Suspicious", 15), ("Pragmatic", 10)]
        },
        "target_state": {
            "ally_a": {"Cooperative": 25, "Suspicious": 25, "Pragmatic": 30, "Cautious": 20},
            "ally_b": {"Cooperative": 25, "Suspicious": 25, "Pragmatic": 30, "Cautious": 20}
        },
        "actions": {
            "pragmatic_proposal": {
                "description": "Предложить сугубо деловое соглашение",
                "author_delta": {"Pragmatic": 12, "Cooperative": 8},
                "target_delta": {"Pragmatic": 10, "Suspicious": -5}
            },
            "verify_honesty": {
                "description": "Проверить честность союзника",
                "author_delta": {"Suspicious": 10, "Cautious": 10},
                "target_delta": {"Suspicious": 8, "Cautious": 8}
            },
            "shared_success": {
                "description": "Достичь успеха вместе",
                "author_delta": {"Cooperative": 15, "Suspicious": -10, "Pragmatic": 8},
                "target_delta": {"Cooperative": 15, "Suspicious": -10, "Pragmatic": 8}
            }
        }
    },

    "hidden_admiration": {
        "name": "Скрытое восхищение",
        "description": "Один участник тайно восхищается другим, но не решается выразить это открыто из-за робости или социальных барьеров",
        "participant_roles": ["admirer", "idol"],
        "conditions": {
            "admirer_to_idol": [("Admiring", 25), ("Respectful", 20), ("Hesitant", 15)],
            "idol_to_admirer": [("Unaware", 20), ("Neutral", 15)] # Идол может быть вообще не в курсе
        },
        "target_state": {
            "admirer": {"Admiring": 35, "Respectful": 25, "Hesitant": 25, "Inspired": 20},
            "idol": {"Unaware": 25, "Neutral": 20, "Confident": 15} # Целевое состояние может не достигаться, если схема не активирована
        },
        "actions": {
            "observe_from_afar": {
                "description": "Наблюдать за объектом восхищения издалека",
                "author_delta": {"Admiring": 8, "Hesitant": 5, "Inspired": 6},
                "target_delta": {} # Идол ничего не замечает
            },
            "attempt_compliment": {
                "description": "Попытаться сделать робкий комплимент",
                "author_delta": {"Hesitant": 10, "Admiring": 8},
                "target_delta": {"Unaware": -5, "Neutral": 5} # Идол может начать что-то подозревать
            },
            "confess_admiration": {
                "description": "Признаться в восхищении (ключевое действие)",
                "author_delta": {"Hesitant": -20, "Admiring": 15, "Respectful": 10},
                "target_delta": {"Unaware": -20, "Flattered": 15, "Surprised": 10}
            }
        }
    },

    "parental_care": {
        "name": "Родительская опека",
        "description": "Асимметричные отношения заботы и защиты, где одна сторона оберегает и направляет другую",
        "participant_roles": ["caregiver", "ward"],
        "conditions": {
            "caregiver_to_ward": [("Protective", 25), ("Nurturing", 20), ("Responsible", 20)],
            "ward_to_caregiver": [("Trusting", 25), ("Dependent", 20), ("Respectful", 15)]
        },
        "target_state": {
            "caregiver": {"Protective": 35, "Nurturing": 30, "Responsible": 30, "Patient": 25},
            "ward": {"Trusting": 35, "Secure": 30, "Respectful": 25, "Obedient": 20}
        },
        "actions": {
            "provide_comfort": {
                "description": "Обеспечить комфорт и безопасность (опекун)",
                "author_delta": {"Nurturing": 12, "Protective": 10},
                "target_delta": {"Secure": 15, "Trusting": 12}
            },
            "set_boundary": {
                "description": "Установить границы (опекун)",
                "author_delta": {"Responsible": 10, "Patient": 8},
                "target_delta": {"Obedient": 10, "Respectful": 8}
            },
            "seek_approval": {
                "description": "Искать одобрения (подопечный)",
                "author_delta": {"Respectful": 10, "Dependent": 8},
                "target_delta": {"Nurturing": 10, "Protective": 8}
            }
        }
    },

    "professional_rivalry": {
        "name": "Профессиональное соперничество",
        "description": "Конкуренция, основанная на взаимном уважении к компетенциям и стремлении к совершенству",
        "participant_roles": ["professional_a", "professional_b"],
        "conditions": {
            "professional_a_to_professional_b": [("Competitive", 20), ("Respectful", 15), ("Driven", 15)],
            "professional_b_to_professional_a": [("Competitive", 20), ("Respectful", 15), ("Driven", 15)]
        },
        "target_state": {
            "professional_a": {"Competitive": 30, "Respectful": 25, "Driven": 30, "Focused": 25},
            "professional_b": {"Competitive": 30, "Respectful": 25, "Driven": 30, "Focused": 25}
        },
        "actions": {
            "challenge_constructively": {
                "description": "Бросить вызов в профессиональной сфере",
                "author_delta": {"Competitive": 10, "Driven": 8},
                "target_delta": {"Competitive": 10, "Driven": 8, "Respectful": 5}
            },
            "acknowledge_skill": {
                "description": "Признать мастерство соперника",
                "author_delta": {"Respectful": 12, "Competitive": 5},
                "target_delta": {"Respectful": 10, "Focused": 8}
            },
            "set_new_standard": {
                "description": "Установить новый стандарт качества",
                "author_delta": {"Driven": 15, "Focused": 12, "Competitive": 10},
                "target_delta": {"Driven": 12, "Competitive": 10}
            }
        }
    },
}
