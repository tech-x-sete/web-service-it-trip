from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)


def load_news():
    with open('news.json', 'r', encoding='utf-8') as f:
        news = json.load(f)
        # Форматируем даты для отображения
        for item in news:
            item['start_date'] = datetime.strptime(item['start_date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            if item['end_date'] != item['start_date']:
                item['end_date'] = datetime.strptime(item['end_date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            else:
                item['end_date'] = None
        return news


@app.route('/')
def newsfeed():
    news = load_news()
    return render_template('newsfeed.html', news=news)


if __name__ == '__main__':
    app.run(debug=True)
