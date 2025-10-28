import aiohttp
import asyncio
import random
from typing import Optional


class WebContentLoader:
    """Загрузчик произведений из Project Gutenberg"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.processed_books = set()  # Отслеживаем уже обработанные книги
    
    async def fetch_random_book(self) -> Optional[tuple]:
        """
        Загрузить случайную книгу из Project Gutenberg
        
        Returns:
            (book_id, text, title) или None
        """
        # Генерируем случайный ID (на Gutenberg ~70000 книг)
        max_attempts = 10
        
        for attempt in range(max_attempts):
            book_id = random.randint(1, 70000)
            
            # Пропускаем уже обработанные
            if book_id in self.processed_books:
                continue
            
            result = await self.load_from_project_gutenberg(book_id)
            if result:
                self.processed_books.add(book_id)
                return (book_id, result[0], result[1])
            
            # Небольшая пауза между попытками
            await asyncio.sleep(1)
        
        return None
    
    async def load_from_project_gutenberg(self, book_id: int) -> Optional[tuple]:
        """Загрузить книгу по ID"""
        urls = [
            f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
            f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
            f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
        ]
        
        for url in urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers, timeout=30) as response:
                        if response.status == 200:
                            text = await response.text()
                            
                            # Проверяем что это не слишком короткий текст
                            if len(text) < 5000:
                                return None
                            
                            # Извлекаем название
                            lines = text.split('\n')[:100]
                            title = f"Book_{book_id}"
                            
                            for line in lines:
                                if 'Title:' in line:
                                    title = line.split('Title:')[-1].strip()
                                    break
                                elif 'TITLE:' in line:
                                    title = line.split('TITLE:')[-1].strip()
                                    break
                            
                            return (text, title)
            except:
                continue
        
        return None
