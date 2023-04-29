import time as t
import requests
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# данные для отправки уведомления в Telegram
BOT_TOKEN = '5837398774:AAH9gKiaTjB9h6V0jQdceuDvhJeKNOJKbOQ'
CHAT_ID = 428276584

url = 'https://fairway.moscow/experts/guzairova-natalya-petrovna'

# создаем пустой список для уникальных дат
dates = []

# создаем экземпляр бота и диспетчера
loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, loop=loop)
dp = Dispatcher(bot)

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Бот запущен и будет проверять расписание каждые 30 минут.')
    # добавляем задание в очередь на выполнение функции check_schedule
    while True:
        await check_schedule()
        await t.sleep(1800)

@dp.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    """Обработчик команды /stop."""
    # Отменяем задание check_schedule, если оно выполняется
    for task in asyncio.all_tasks():
        if task.get_name() == 'check_schedule':
            task.cancel()
    # Запускаем send_response() в отдельной задаче
    asyncio.create_task(send_response(message))

async def send_response(message: types.Message):
    """Отправляет ответное сообщение."""
    await message.answer('Бот остановлен.', reply_markup=types.ReplyKeyboardRemove())


# функция для проверки расписания
async def check_schedule():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    day_schedule = soup.find_all(class_='time')

    if day_schedule:
        new_dates = []
        for day in day_schedule:
            # преобразуем строку в объект datetime
            time = datetime.strptime(day.text, '%H:%M')
            # создаем объект datetime с текущей датой и временем из расписания
            now = datetime.now().replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
            # преобразуем объект datetime в нужный формат
            formatted_date = now.strftime('%Y-%m-%d %H:%M')
            # добавляем уникальные даты в список
            if formatted_date not in dates:
                dates.append(formatted_date)
                new_dates.append(formatted_date)

        # если есть новые даты, отправляем уведомление
        if new_dates:
            message = 'Найдены новые даты в расписании: {}\nНовые даты:\n{}'.format(url, '\n'.join(new_dates))
            await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
