from flask import Flask, render_template
from endpoints.publications_endpoints import publications_bp

app = Flask(__name__)
app.register_blueprint(publications_bp, url_prefix='/publications')


if __name__ == '__main__':
    app.run(debug=True)
