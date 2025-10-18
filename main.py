import asyncio
from aiogram import Bot, Dispatcher
import threading
import time

from config import API_TOKEN
from emotions.models import emotion_model
from handlers.message_handlers import setup_handlers
from moral_schemas.manager import MoralSchemaManager

def admin_console():
    """Консоль админа для просмотра состояния системы"""
    schema_manager = MoralSchemaManager()
    
    while True:
        print("\n🔒 [ADMIN CONSOLE] Выберите действие:")
        print("1 - Показать отчет об отношениях")
        print("2 - Показать активные схемы")
        print("3 - Статистика системы")
        print("4 - Выход")
        
        try:
            choice = input("Введите номер: ").strip()
            
            if choice == "1":
                emotion_model.print_relations_report()
            elif choice == "2":
                schema_manager.print_active_schemas_report()
            elif choice == "3":
                print(f"🔒 [ADMIN] Всего отношений: {len(emotion_model.relations)}")
                print(f"🔒 [ADMIN] Активных схем: {len(schema_manager.active_schemas)}")
                
                # Статистика по участникам
                user_ids = set()
                for (from_id, to_id) in emotion_model.relations.keys():
                    user_ids.add(from_id)
                    user_ids.add(to_id)
                user_ids.discard(-1)  # Убираем агента
                print(f"🔒 [ADMIN] Участников в системе: {len(user_ids)}")
                
            elif choice == "4":
                break
            else:
                print("🔒 [ADMIN] Неверный выбор")
        except Exception as e:
            print(f"🔒 [ADMIN] Ошибка в консоли админа: {e}")

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    # Настраиваем обработчики
    await setup_handlers(dp, bot)
    
    print("🔒 [ADMIN] 🤖 Бот запущен в режиме эксперимента")
    print("🔒 [ADMIN] Вся аналитика доступна только исследователям")
    print("🔒 [ADMIN] Для доступа к консоли админа введите команды в консоли")
    
    # Запускаем консоль админа в отдельном потоке
    admin_thread = threading.Thread(target=admin_console, daemon=True)
    admin_thread.start()
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"🔒 [ADMIN] Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())