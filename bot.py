import time as t
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# данные для отправки уведомления в Telegram
BOT_TOKEN = '5837398774:AAH9gKiaTjB9h6V0jQdceuDvhJeKNOJKbOQ'
CHAT_ID = '428276584'

url = 'https://fairway.moscow/experts/verbitskaya-mariya'

# создаем пустой список для уникальных дат
dates = []



while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    day_schedule = soup.find_all(class_='time')

    if day_schedule:
        new_dates = []
        for day in day_schedule:
            # преобразуем строку в объект datetime
            time = datetime.strptime(day.text, '%H:%M')
            # создаем о��ъект datetime с текущей датой и временем из расписания
            now = datetime.now().replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
            # преобразуем объект datetime в нужный формат
            formatted_date = now.strftime('%Y-%m-%d %H:%M')
            # добавляем уникальные даты в список
            if formatted_date not in dates:
                dates.append(formatted_date)
                new_dates.append(formatted_date)

        # если есть новые даты, отправляем уведомление
        if new_dates:
            message = 'Найдены новые даты в расписании: {}\nНовые д��ты:\n{}'.format(url, '\n'.join(new_dates))
            telegram_api_url = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_TOKEN)
            data = {'chat_id': CHAT_ID, 'text': message}
            response = requests.post(telegram_api_url, data=data)
            print('Уведомление отправлено в Telegram:', response.json())

    t.sleep(300) # ждем 5 минут перед следующей проверкой
