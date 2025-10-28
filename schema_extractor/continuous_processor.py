import asyncio
import signal
import os
from datetime import datetime
from schema_extractor.web_loader import WebContentLoader
from schema_extractor.extractor import MoralSchemaExtractor


class ContinuousSchemaExtractor:
    """Непрерывный экстрактор моральных схем"""
    
    def __init__(self, 
                 output_file: str = "moral_schemas/schemas.py",
                 backup_file: str = "moral_schemas/schemas_auto.py"):
        self.loader = WebContentLoader()
        self.extractor = MoralSchemaExtractor()
        self.output_file = output_file
        self.backup_file = backup_file
        
        self.all_schemas = {}
        self.books_processed = 0
        self.schemas_found = 0
        self.running = True
        
        # Загружаем существующие схемы
        self._load_existing_schemas()
        
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _load_existing_schemas(self):
        """Загрузить существующие схемы из файла"""
        if os.path.exists(self.output_file):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("schemas", self.output_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'MORAL_SCHEMAS'):
                    self.all_schemas = dict(module.MORAL_SCHEMAS)
                    print(f"✅ Загружено существующих схем: {len(self.all_schemas)}")
            except Exception as e:
                print(f"⚠️  Не удалось загрузить существующие схемы: {e}")
    
    def _signal_handler(self, signum, frame):
        """Обработка Ctrl+C"""
        print("\n\n⚠️  Получен сигнал остановки...")
        self.running = False
    
    async def process_one_book(self):
        """Обработать одну книгу"""
        result = await self.loader.fetch_random_book()
        
        if not result:
            print("⚠️  Не удалось загрузить книгу, пробую ещё...")
            await asyncio.sleep(5)
            return
        
        book_id, text, title = result
        self.books_processed += 1
        
        print(f"\n{'='*70}")
        print(f"📖 [{self.books_processed}] {title} (ID: {book_id})")
        print(f"{'='*70}")
        
        chunks = [text[i:i+3000] for i in range(0, min(len(text), 9000), 3000)]
        
        new_schemas_count = 0
        
        for i, chunk in enumerate(chunks, 1):
            print(f"  📄 Фрагмент {i}/{len(chunks)}...")
            
            schemas = await self.extractor.extract_schemas_from_text(chunk, title)
            
            if schemas:
                for schema in schemas:
                    key = schema.get('schema_key', self.extractor._generate_key(schema.get('name', '')))
                    schema['schema_key'] = key
                    
                    if key not in self.all_schemas:
                        self.all_schemas[key] = schema
                        new_schemas_count += 1
                        self.schemas_found += 1
                        print(f"    ✅ Новая: {schema.get('name')}")
            
            await asyncio.sleep(2)
        
        if new_schemas_count > 0:
            print(f"\n  📊 Новых схем: {new_schemas_count}")
            self._save_progress()
        else:
            print(f"\n  ⚠️  Новых схем не найдено")
        
        self._print_stats()
    
    def _save_progress(self):
        """Сохранить прогресс"""
        schemas_list = list(self.all_schemas.values())
        
        # Сохраняем в основной файл
        self.extractor.save_schemas_to_file(schemas_list, self.output_file)
        print(f"  💾 Основной файл: {self.output_file}")
        
        # Сохраняем бэкап
        self.extractor.save_schemas_to_file(schemas_list, self.backup_file)
        print(f"  💾 Бэкап: {self.backup_file}")
    
    def _print_stats(self):
        """Статистика"""
        print(f"\n  📈 Обработано: {self.books_processed} книг | Схем: {len(self.all_schemas)}")
    
    async def run(self):
        """Главный цикл"""
        print("\n" + "="*70)
        print("🔄 АВТОМАТИЧЕСКИЙ ЭКСТРАКТОР МОРАЛЬНЫХ СХЕМ")
        print("="*70)
        print("📚 Источник: Project Gutenberg (70000+ книг)")
        print("🤖 Непрерывная работа до нажатия Ctrl+C")
        print(f"💾 Файл схем: {self.output_file}")
        print(f"💾 Бэкап: {self.backup_file}")
        print("="*70)
        
        start_time = datetime.now()
        
        while self.running:
            try:
                await self.process_one_book()
                
                if self.running:
                    print(f"\n⏳ Пауза 5 секунд...")
                    await asyncio.sleep(5)
            
            except Exception as e:
                print(f"\n❌ Ошибка: {e}")
                await asyncio.sleep(10)
        
        # Финал
        print("\n" + "="*70)
        print("🛑 ЗАВЕРШЕНИЕ РАБОТЫ")
        print("="*70)
        
        if self.all_schemas:
            self._save_progress()
        
        duration = datetime.now() - start_time
        hours = duration.total_seconds() / 3600
        
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   ⏱️  Время работы: {hours:.2f} часов")
        print(f"   📚 Обработано книг: {self.books_processed}")
        print(f"   ✨ Найдено схем: {self.schemas_found}")
        print(f"   🎯 Уникальных схем: {len(self.all_schemas)}")
        
        if self.all_schemas:
            print(f"\n📋 ТОП-10 СХЕМ:")
            for i, (key, schema) in enumerate(list(self.all_schemas.items())[:10], 1):
                print(f"   {i}. {schema.get('name')} ({key})")
        
        print(f"\n✅ Схемы сохранены в:")
        print(f"   • {self.output_file}")
        print(f"   • {self.backup_file}")
        print("\n👋 Готово!")


async def main():
    """Точка входа"""
    print("\n🎯 РЕЖИМ РАБОТЫ:")
    print("1 - Добавлять в основной файл (schemas.py) - используется ботом")
    print("2 - Создать отдельный файл (schemas_auto.py)")
    
    choice = input("\n👉 Ваш выбор (Enter = 1): ").strip() or "1"
    
    if choice == "1":
        extractor = ContinuousSchemaExtractor(
            output_file="moral_schemas/schemas.py",
            backup_file="moral_schemas/schemas_backup.py"
        )
    else:
        extractor = ContinuousSchemaExtractor(
            output_file="moral_schemas/schemas_auto.py",
            backup_file="moral_schemas/schemas_backup.py"
        )
    
    await extractor.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Остановлено")
