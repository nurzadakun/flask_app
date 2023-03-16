from flask import Flask, render_template, request
import sqlite3
import hashlib
import random
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nurzada670@gmail.com'
app.config['MAIL_PASSWORD'] = 'wxtcbdbyciknjgqt'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route("/")
def welcome():
    return render_template("index.html", name="1")

#регистрация

@app.route("/regist", methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']

        password = hash_password(password)

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        cursor.execute('''INSERT INTO users (login, email, password)
        VALUES ('%s', '%s', '%s')
        '''%(login, email, password))

        connect.commit()
        connect.close()
    return render_template("regist.html")

def hash_password(password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password


@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        password = hash_password(password)

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM USERS WHERE login='%s' AND password='%s'"%(login, password))
        user = cursor.fetchall()

        print(user)

        if user:
            if(user[0][3]==password):
                return render_template("welcome.html", login=login)
            
        connect.commit()
        connect.close()
    return render_template("auth.html")

def generate_random_number():
    number = random.randint(10000, 99999)
    return number


@app.route("/forgot_password", methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        msg = Message('Восстановление пароля', sender = 'flask_first_app', recipients = [email])
        msg.body = "Перейдите по ссылке чтобы восстановить пароль"
        mail.send(msg)

    return render_template("forgotpassword.html")

