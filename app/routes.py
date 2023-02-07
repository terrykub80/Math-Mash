from app import app

@app.route('/')
def index():
    return '###Welcome to Math Mash!'

@app.route('/scores')
def posts():
    return 'These are the scores!'
