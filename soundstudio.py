from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import magic
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'flythonestudio@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_PASSWORD'] = 'kymswmsqdgvkhbhs'  # введите пароль
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
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.username}-{self.email}"

def create_admin_user():
    admin_username = 'admin3'
    admin_email = 'admin3@example.com'
    admin_password = generate_password_hash('1234')
    existing_user = User.query.filter_by(email=admin_email).first()
    if existing_user:
        return
    admin_user = User(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.String(5), nullable=False)
with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'mp3', 'wav'}  # Дозволені розширення файлів

def allowed_file(filename):
    """Перевіряє, чи є файл з даним ім'ям дозволеним за його розширенням."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
    return render_template('home.html')


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
            sender = 'flythonestudio@gmail.com'
            msg = Message('Новий демозапис', sender=sender, recipients=['flythonestudio@gmail.com'])
            msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nFile: {file.filename}"
            msg.attach(
                filename=file.filename,
                content_type='application/octet-stream',
                data=file_data,)
            try:
                mail.send(msg)
                return render_template('studio/sent_demo.html')
            except Exception as e:
                print(e)
                return 'the email was not sent.'
        else:
            # Якщо файл заборонений, виводимо повідомлення
            return "File extension not allowed, please select an MP3 or WAV file."
    else:
        return render_template('studio/send_demo.html')

@app.route('/showroom')
def showroom():
    return render_template('showroom/contacts_showroom.html')


@app.route('/store')
def store():
    return render_template('showroom/store.html')


@app.route('/contacts_showroom')
def about_showroom():
    return render_template('showroom/contacts_showroom.html')

@app.route('/login_showroom', methods=['POST', 'GET'])
def login_showroom():
    # Check if user is already logged in
    if session.get('current_user'):
        return redirect(url_for('store'))

    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form.get('password')

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # If the password is correct, store the user ID in the session
            session['current_user'] = user.id

            # Check if the user is an admin
            if user.is_admin:
                session['is_admin'] = True
            else:
                session['is_admin'] = False

            return redirect(url_for('store'))
        else:
            return "Wrong email or password. Please try again."


    return render_template('showroom/login_showroom.html')

@app.route('/logout')
def logout():
    if not session.get('is_admin'):
        return 'Access denied'
    # Видаляємо сеансову змінну `current_user`
    session.pop('current_user', None)
    # Видаляємо сеансову змінну `is_admin`
    session.pop('is_admin', None)
    return redirect(url_for('home'))


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    # Отримуємо дані з форми
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])

    # Створюємо новий товар
        item = Item(name=name, size=size, price=price, quantity=quantity)

    # Додаємо товар до бази даних
        db.session.add(item)
        db.session.commit()

    # Перенаправляємо користувача на сторінку "/store"
        return redirect(url_for('store'))
    else:
        return render_template('showroom/add_item.html')


if __name__ == '__main__':
    create_admin_user()
    app.run(debug=True)
