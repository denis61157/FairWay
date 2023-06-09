import calendar
from datetime import datetime
import time as t
import requests

from bs4 import BeautifulSoup


# данные для отправки уведомления в Telegram
BOT_TOKEN = '5837398774:AAH9gKiaTjB9h6V0jQdceuDvhJeKNOJKbOQ'
CHAT_ID = '1001962172474'

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
            formatted_date = day.attrs['data-time']
            week_day = calendar.day_name[datetime.strptime(formatted_date.split()[0], '%Y-%m-%d').weekday()]
            # добавляем уникальные даты в список
            key = f'{week_day} {formatted_date}'
            if key not in dates:
                dates.append(key)
                new_dates.append(key)

        # если есть новые даты, отправляем уведомление
        if new_dates:
            message = 'Найдены новые даты в расписании: {}\nНовые даты:\n{}'.format(url, '\n'.join(new_dates))
            telegram_api_url = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_TOKEN)
            data = {'chat_id': CHAT_ID, 'text': message}
            response = requests.post(telegram_api_url, data=data)
            print('Уведомление отправлено в Telegram:', response.json())

    t.sleep(300)  # ждем 5 минут перед следующей проверкой
