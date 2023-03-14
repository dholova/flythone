from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studio.db'
db = SQLAlchemy(app)


class Signing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/studio')
def studio():
    return render_template('studio.html')


@app.route('/send_demo')
def send_demo():
    return render_template('send_demo.html')


if __name__ == '__main__':
    app.run(debug=True)
