from flask import Flask, render_template, request, url_for, redirect, session
import hashlib
import random
from flask_mail import Mail, Message
from flask_session import Session
from flask_socketio import SocketIO, emit
import db_context
from datetime import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nurzada670@gmail.com'
app.config['MAIL_PASSWORD'] = 'wxtcbdbyciknjgqt'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route("/")
def welcome():
    if not session.get("name"):
        return render_template('index.html')
    users = db_context.db_context("Select * from users where users.login <> '%s'"%session["name"])
    print('hjfvhvk', users)
    return render_template('profile.html', login=session["name"], users = users)

#регистрация

@app.route("/regist", methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']

        password = hash_password(password)

        db_context.db_context('''INSERT INTO users (login, email, password)
        VALUES ('%s', '%s', '%s')
        '''%(login, email, password), commit=True)

    return render_template("regist.html")

#зашифровка пароля
def hash_password(password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password

#авторизация
@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        password = hash_password(password)

        user = db_context.db_context("SELECT * FROM USERS WHERE login='%s' AND password='%s'"%(login, password))
        if user:
            if(user[0][3]==password):
                session["name"] = login
                session["user_id"] = user[0][0]
                return render_template("profile.html", login=login)
            
    return render_template("auth.html")

#создание рандомного числа 
def generate_random_number():
    number = random.randint(10000, 99999)
    return number

#запрос на изменение пароля, отправка письма на почту
@app.route("/forgot_password", methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        user = db_context.db_context("SELECT * FROM users WHERE email = '%s'"%(email))

        if user:
            token = generate_random_number()  

            
            db_context.db_context("UPDATE users SET reset_token = '%s' WHERE email = '%s'"%(token, email))

            link = url_for('reset', token=token)
            msg = Message('Восстановление пароля', sender = 'flask_first_app', recipients = [email])
            msg.body = f"Перейдите по ссылке чтобы восстановить пароль: http://localhost:5000{link}"
            mail.send(msg)

            return render_template("auth.html")
    return render_template("forgotpassword.html")

#изменение пароля
@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset(token):
    if request.method == 'POST':
        db_context.db_context("SELECT * FROM users WHERE reset_token = '%s'"%(token))

        password = request.form['new_password']
        password = hash_password(password)

        db_context.db_context("UPDATE users SET password = '%s', reset_token = NULL WHERE id = '%s'"%(password, user[0]))
        
        return redirect("/auth")
    return render_template("resetpassword.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


@app.route('/chat/<user_id>')
def chat(user_id):
    print('dsvfds', user_id)
    return render_template('chat.html', user_id_receiver = user_id)

@socketio.on('send')
def handle_send(data):
    curDT = datetime.now()
    message = data['message']
    user_id_receiver = data['user_id_receiver']
    db_context.db_context('''
        INSERT INTO messages (user_id_sender, user_id_receiver, message_text, message_datetime)
        VALUES (%s, %s, '%s', '%s')
    '''%(session["user_id"], user_id_receiver, message, curDT.strftime("%m/%d/%Y, %H:%M:%S")),commit=True)
    print('ffffff', message)
    socketio.emit('message', {'message': message})

if __name__ == '__main__':
    socketio.run(app)