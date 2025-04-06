import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

API_TOKEN = '8074629111:AAEfcNmRRDAW29K4EjOnBv3ae3js16JsKEE'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Списки жанров и книг
genres_books = {
    "📚 Фантастика": [
        {"Название": "1984", "Ссылка": "https://mybook.ru/author/dzhordzh-oruell/1984/read/"},
        {"Название": "Дюна", "Ссылка": "https://www.litres.ru/book/frenk-gerbert/duna-55339991/chitat-onlayn/"},
        {"Название": "451 градус по Фаренгейту", "Ссылка": "https://www.litres.ru/book/rey-bredberi/451-gradus-po-farengeytu-39507162/chitat-onlayn/"}
    ],
    "🧙‍♂️ Фэнтези": [
        {"Название": "Властелин колец", "Ссылка": "http://loveread.me/series-books.php?id=33"},
        {"Название": "Гарри Поттер ", "Ссылка": "http://loveread.ec/series-books.php?id=12"},
        {"Название": "Хоббит", "Ссылка": "https://www.litres.ru/book/dzhon-tolkin/hobbit-ili-tuda-i-obratno-122257/chitat-onlayn/"}
    ],
    "🕵️‍♂️ Детектив": [
        {"Название": "Шерлок Холмс: Этюд в багровых тонах", "Ссылка": "http://loveread.ec/view_global.php?id=6970"},
        {"Название": "Убийство в Восточном экспрессе", "Ссылка": "http://loveread.ec/view_global.php?id=2651"},
        {"Название": "Код да Винчи", "Ссылка": "http://loveread.ec/view_global.php?id=2331"}
    ],
    "📖 Классика": [
        {"Название": "Война и мир", "Ссылка": "https://ilibrary.ru/text/11/index.html"},
        {"Название": "Преступление и наказание", "Ссылка": "https://ilibrary.ru/text/69/p.1/index.html"},
        {"Название": "Анна Каренина", "Ссылка": "https://ilibrary.ru/text/1099/index.html"}
    ],
    "❤️ Романтика": [
        {"Название": "Гордость и предубеждение", "Ссылка": "https://www.litres.ru/book/dzheyn-ostin/gordost-i-predubezhdenie-6257491/chitat-onlayn/"},
        {"Название": "Три товарища", "Ссылка": "http://litres.ru/book/erih-mariya-remark/tri-tovarischa-32544665/chitat-onlayn/"},
        {"Название": "Я до тебя", "Ссылка": "https://litgorod.ru/books/view/19507"}
    ],
    "👻 Ужасы": [
        {"Название": "Оно", "Ссылка": "http://loveread.ec/contents.php?id=1635"},
        {"Название": "Сияние", "Ссылка": "http://loveread.ec/contents.php?id=988"},
        {"Название": "Кладбище домашних животных", "Ссылка": "http://loveread.ec/view_global.php?id=1468"}
    ],
    "🔬 Научная литература": [
        {"Название": "Краткая история времени", "Ссылка": "http://loveread.ec/view_global.php?id=73472"},
        {"Название": "Сапиенс", "Ссылка": "http://loveread.ec/read_book.php?id=57922&p=1"},
        {"Название": "Космос", "Ссылка": "http://loveread.ec/view_global.php?id=73378"}
    ]
}

# Создаём клавиатуру для выбора жанра
genre_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=genre, callback_data=f"genre_{genre}")] for genre in genres_books.keys()
    ]
)

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    """Обработчик команды /start."""
    await message.answer(
        "Привет! Выберите жанр из кнопок ниже, чтобы увидеть список книг.",
        reply_markup=genre_keyboard
    )

@dp.callback_query(lambda callback: callback.data.startswith("genre_"))
async def genre_handler(callback: types.CallbackQuery):
    """Обработчик выбора жанра."""
    genre = callback.data.split("_")[1]
    books = genres_books.get(genre, [])
    if books:
        book_list = "\n\n".join([f"📖 {book['Название']}\n🔗 {book['Ссылка']}" for book in books])
        await callback.message.answer(f"Вот книги в жанре '{genre}':\n\n{book_list}")
    else:
        await callback.message.answer("Книги в этом жанре не найдены.")
    await callback.answer()

async def main():
    """Запуск бота."""
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")

if __name__ == "__main__":
    asyncio.run(main())
