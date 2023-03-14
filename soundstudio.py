from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Head page'


@app.route('/home')
def home():
    return 'Оберіть послугу'

if __name__ == '__main__':
    app.run(debug=True)
