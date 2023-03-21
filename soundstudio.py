from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import magic
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'afolenko1991@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_PASSWORD'] = 'rhwyscthqxxzvknk'  # введите пароль
db = SQLAlchemy(app)
mail = Mail(app)
class SendDemo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Text, nullable=False)
    file = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<SendDemo %r>' % self.id
with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'mp3', 'wav'}  # Дозволені розширення файлів

def allowed_file(filename):
    """Перевіряє, чи є файл з даним ім'ям дозволеним за його розширенням."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/names')
def names():
    demos = SendDemo.query.order_by(SendDemo.date).all()
    return render_template('names.html', demos=demos)


@app.route('/studio')
def studio():
    return render_template('studio/studio.html')


@app.route('/equipment')
def equipment():
    return render_template('studio/equipment.html')

@app.route('/works')
def works():
    return render_template('studio/works.html')

@app.route('/price')
def price():
    return render_template('studio/price.html')

@app.route('/contacts')
def contacts():
    return render_template('studio/contacts.html')


@app.route("/send_demo", methods=['POST', 'GET'])
def send_demo():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        file = request.files['file']
        if not file:
            return "File not found in request"
        if file and allowed_file(file.filename):
            file_data = file.read()
            article = SendDemo(name=name, email=email, phone=phone, file=file_data)
            db.session.add(article)
            db.session.commit()
            sender = 'afolenko1991@gmail.com'
            msg = Message('Новий демозапис', sender=sender, recipients=['afolenko1991@gmail.com'])
            msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nFile: {file.filename}"
            msg.attach(
                filename=file.filename,
                content_type='application/octet-stream',
                data=file_data,)
            try:
                mail.send(msg)
                return 'Email sent...'
            except Exception as e:
                print(e)
                return 'the email was not sent.'
        else:
            # Якщо файл заборонений, виводимо повідомлення
            return "File extension not allowed, please select an MP3 or WAV file."
    else:
        return render_template('studio/send_demo.html')



if __name__ == '__main__':
    app.run(debug=True)
