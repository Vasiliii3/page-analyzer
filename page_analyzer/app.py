from flask import Flask

# Это уже нам знакомое callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


if __name__ == "__main__":
    app.run()
