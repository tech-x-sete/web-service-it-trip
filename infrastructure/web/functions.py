import json
from datetime import datetime


def load_news():
    with open('../../news.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
        # Форматируем даты для отображения
        for item in news:
            item['start_date'] = datetime.strptime(item['start_date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            if item['end_date'] != item['start_date']:
                item['end_date'] = datetime.strptime(item['end_date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            else:
                item['end_date'] = None

        return news
