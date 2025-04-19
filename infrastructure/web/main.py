from flask import Flask, render_template
import functions

app = Flask(__name__)


# Разбить все роуты на роли


@app.route('/', '/main')
def newsfeed():
    news = functions.load_news()
    return render_template('newsfeed.html', news=news)


@app.route('/add_writer')
def add_writer():
    ...


@app.route('/delete_writer')
def delete_writer():
    ...


@app.route('/add_title')
def add_title():
    ...


@app.route('/delete_title')
def delete_title():
    ...


if __name__ == '__main__':
    app.run(debug=True)
