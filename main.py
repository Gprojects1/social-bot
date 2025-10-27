import asyncio
from aiogram import Bot, Dispatcher
import threading

from config import API_TOKEN, AI_AGENT_VIRTUAL_ID
from emotions.models import emotion_model
from handlers.message_handlers import setup_handlers
from moral_schemas.manager import MoralSchemaManager
from database.chat_db import chat_db


def admin_console():
    """Консоль админа для просмотра состояния системы"""
    schema_manager = MoralSchemaManager()
    
    while True:
        print("\n🔒 [ADMIN CONSOLE] Выберите действие:")
        print("1 - Показать отчет об отношениях")
        print("2 - Показать активные схемы")
        print("3 - Статистика системы")
        print("4 - Список участников виртуального чата")
        print("5 - Выход")
        
        try:
            choice = input("Введите номер: ").strip()
            
            if choice == "1":
                emotion_model.print_relations_report()
            
            elif choice == "2":
                if hasattr(schema_manager, 'print_active_schemas_report'):
                    schema_manager.print_active_schemas_report()
                else:
                    print("\n" + "="*70)
                    print("📋 АКТИВНЫЕ МОРАЛЬНЫЕ СХЕМЫ")
                    print("="*70)
                    if schema_manager.active_schemas:
                        for (user1, user2), schema_key in schema_manager.active_schemas.items():
                            print(f"Схема: {schema_key}")
                            print(f"Участники (виртуальные ID): {user1} ↔ {user2}")
                    else:
                        print("Нет активных схем")
                    print("="*70)
            
            elif choice == "3":
                print(f"\n🔒 [ADMIN] === СТАТИСТИКА СИСТЕМЫ ===")
                print(f"🔒 [ADMIN] Всего отношений: {len(emotion_model.relations)}")
                print(f"🔒 [ADMIN] Активных схем: {len(schema_manager.active_schemas)}")
                
                virtual_ids = set()
                for (from_id, to_id) in emotion_model.relations.keys():
                    virtual_ids.add(from_id)
                    virtual_ids.add(to_id)
                
                print(f"🔒 [ADMIN] Участников с отношениями: {len(virtual_ids)}")
                print(f"🔒 [ADMIN] Виртуальный ID агента: {AI_AGENT_VIRTUAL_ID}")
                
            elif choice == "4":
                print("\n" + "="*70)
                print("👥 УЧАСТНИКИ ВИРТУАЛЬНОГО ЧАТА")
                print("="*70)
                
                participants = chat_db.get_all_participants()
                
                if not participants:
                    print("Нет зарегистрированных участников")
                else:
                    for p in participants:
                        is_ai = " [🤖 ИИ АГЕНТ]" if p['virtual_id'] == AI_AGENT_VIRTUAL_ID else ""
                        print(f"Virtual ID {p['virtual_id']}: Telegram ID {p['telegram_id']} (@{p.get('username', 'Unknown')}){is_ai}")
                
                print("="*70)
            
            elif choice == "5":
                print("🔒 [ADMIN] Выход из консоли")
                break
            
            else:
                print("🔒 [ADMIN] Неверный выбор")
        
        except Exception as e:
            print(f"🔒 [ADMIN] Ошибка в консоли админа: {e}")
            import traceback
            traceback.print_exc()


async def main():
    # УПРОЩЁННОЕ РЕШЕНИЕ: создаём бот без кастомной сессии
    # Используем стандартный таймаут, но увеличенный через параметры
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    # Регистрируем ИИ агента в виртуальном чате
    from config import AI_AGENT_REAL_ID
    ai_virtual_id = chat_db.register_participant(AI_AGENT_REAL_ID, "AI_Agent")
    
    if ai_virtual_id != AI_AGENT_VIRTUAL_ID:
        print(f"⚠️  [ADMIN] ВНИМАНИЕ: Виртуальный ID агента ({ai_virtual_id}) не совпадает с ожидаемым ({AI_AGENT_VIRTUAL_ID})")
        print(f"⚠️  [ADMIN] Обновите AI_AGENT_VIRTUAL_ID в config.py на {ai_virtual_id}")
    
    # Настраиваем обработчики
    await setup_handlers(dp, bot)
    
    print("\n" + "="*70)
    print("🔒 [ADMIN] 🤖 Виртуальный чат-бот запущен!")
    print("="*70)
    print(f"🔒 [ADMIN] Режим: Виртуальный чат (участники не знают, кто ИИ)")
    print(f"🔒 [ADMIN] Виртуальный ID агента: {AI_AGENT_VIRTUAL_ID}")
    print(f"🔒 [ADMIN] Вся аналитика доступна только в админ-консоли")
    print("="*70)
    
    # Запускаем консоль админа в отдельном потоке
    admin_thread = threading.Thread(target=admin_console, daemon=True)
    admin_thread.start()
    
    try:
        print("🔒 [ADMIN] Бот начинает polling...")
        # ИСПРАВЛЕНИЕ: указываем увеличенный request_timeout
        await dp.start_polling(
            bot, 
            skip_updates=True,
            polling_timeout=60,  # Таймаут между запросами
            request_timeout=90   # Таймаут для отдельного запроса
        )
    except Exception as e:
        print(f"🔒 [ADMIN] Ошибка при запуске бота: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # ИСПРАВЛЕНИЕ для Windows: использовать ProactorEventLoop
    if asyncio.sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())
