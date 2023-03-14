from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/studio')
def studio():
    return render_template('studio.html')

if __name__ == '__main__':
    app.run(debug=True)
