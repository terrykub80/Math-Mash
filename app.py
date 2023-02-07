from flask import Flask

app = Flask(__app__)

@app.route('/')
def index():
    x = 10 / 0
    return 'Hello World!!!'