from flask import Flask, render_template

import functions

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/main', methods=['GET'])
def newsfeed():
    news = functions.load_news()
    return render_template('newsfeed.html', news=news)


if __name__ == '__main__':
    app.run(debug=True)
