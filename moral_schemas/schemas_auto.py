# Схем: 6

MORAL_SCHEMAS = {
    "финансовая_опека": {
        "name": "Финансовая опека",
        "description": "Забота о финансовой безопасности через доверительные отношения",
        "participant_roles": ["advisor", "client"],
        "conditions": {"advisor_to_client": [["Trusting", 20], ["Responsible", 15]], "client_to_advisor": [["Trusting", 25], ["Grateful", 15]]},
        "target_state": {"advisor": {"Responsible": 30, "Supportive": 25}, "client": {"Trusting": 35, "Relieved": 20}},
        "actions": {
            "successful_advice": {
                "description": "Успешная финансовая помощь и защита",
                "author_delta": {"Confident": 10, "Responsible": 10},
                "target_delta": {"Trusting": 15, "Grateful": 10}
            }
        }
    },
    "социальная_эмпатия": {
        "name": "Социальная эмпатия",
        "description": "Проявление заботы и интереса к эмоциональному состоянию других",
        "participant_roles": ["observer", "subject"],
        "conditions": {"observer_to_subject": [["Empathetic", 20], ["Curious", 15]], "subject_to_observer": [["Vulnerable", 20], ["Respectful", 15]]},
        "target_state": {"observer": {"Empathetic": 30, "Supportive": 20}, "subject": {"Vulnerable": 25, "Trusting": 20}},
        "actions": {
            "emotional_observation": {
                "description": "Замечание эмоционального состояния и проявление интереса",
                "author_delta": {"Empathetic": 10, "Curious": 5},
                "target_delta": {"Vulnerable": 10, "Respectful": 5}
            }
        }
    },
    "научный_прорыв_и_энтузиазм": {
        "name": "Научный прорыв и энтузиазм",
        "description": "Ученый испытывает восторг от успешного эксперимента",
        "participant_roles": ["professor", "assistant"],
        "conditions": {"professor_to_assistant": [["Enthusiastic", 25], ["Playful", 20]], "assistant_to_professor": [["Cautious", 20], ["Amused", 15]]},
        "target_state": {"professor": {"Enthusiastic": 35, "Confident": 25}, "assistant": {"Trusting": 20, "Supportive": 15}},
        "actions": {
            "successful_experiment": {
                "description": "Демонстрация оживленного животного",
                "author_delta": {"Enthusiastic": 15, "Confident": 10},
                "target_delta": {"Amused": 10, "Cautious": 5}
            }
        }
    },
    "профессиональное_соперничество": {
        "name": "Профессиональное соперничество",
        "description": "Конфликт между традиционным и новым врачом",
        "participant_roles": ["new_doctor", "established_doctor"],
        "conditions": {"new_doctor_to_established_doctor": [["Confident", 20], ["Competitive", 25]], "established_doctor_to_new_doctor": [["Disrespectful", 20], ["Defensive", 15]]},
        "target_state": {"new_doctor": {"Bold": 25, "Determined": 20}, "established_doctor": {"Distrustful": 25, "Confident": 15}},
        "actions": {
            "professional_confrontation": {
                "description": "Публичное исправление коллеги",
                "author_delta": {"Competitive": 10, "Bold": 10},
                "target_delta": {"Disrespectful": 10, "Defensive": 10}
            }
        }
    },
    "научное_служение": {
        "name": "Научное служение",
        "description": "Ученый жертвует личным комфортом ради помощи другим",
        "participant_roles": ["professor", "patient"],
        "conditions": {"professor_to_patient": [["Responsible", 20], ["Supportive", 15]], "patient_to_professor": [["Trusting", 20], ["Grateful", 15]]},
        "target_state": {"professor": {"Responsible": 30, "Supportive": 25}, "patient": {"Trusting": 30, "Grateful": 25}},
        "actions": {
            "self_sacrifice": {
                "description": "Преодоление слабости ради помощи",
                "author_delta": {"Responsible": 10},
                "target_delta": {"Trusting": 10}
            }
        }
    },
    "профессиональная_помощь": {
        "name": "Профессиональная помощь",
        "description": "Эксперт оказывает услугу за вознаграждение",
        "participant_roles": ["expert", "client"],
        "conditions": {"expert_to_client": [["Confident", 20], ["Responsible", 15]], "client_to_expert": [["Trusting", 20], ["Respectful", 15]]},
        "target_state": {"expert": {"Confident": 30, "Responsible": 25}, "client": {"Trusting": 30, "Respectful": 25}},
        "actions": {
            "successful_service": {
                "description": "Выполнение работы с результатом",
                "author_delta": {"Confident": 10},
                "target_delta": {"Trusting": 10}
            }
        }
    }
}
