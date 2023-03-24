from flask import render_template, session, redirect, request, url_for
import db_context, functions
from datetime import datetime
from main import socketio, mail
from flask_mail import Message


#профиль
#session["name"] - это логин пользователя
def welcome():

    #если пользователь не прошел авторизацию его перекидывает на index.html
    if not session.get("name"):
        return render_template('index.html')
    
    users = db_context.db_context("Select * from users where users.login <> '%s'"%session["name"])
    return render_template('profile.html', login=session["name"], users = users)


#чат с другим пользователе
#user_id - это id собеседника, session["user_id"] - это id пользователя
def chat(user_id):

    #если пользователь не прошел авторизацию его перекидывает на index.html
    if not session.get("name"):
        return render_template('index.html')
    
    #вытаскивает логин пользователя, сообщение, время отправки из БД
    messages = db_context.db_context('''Select users.login, messages.message_text, messages.message_datetime from users, messages 
        where users.id=messages.user_id_sender and ((messages.user_id_sender = %s and messages.user_id_receiver = %s)
        or (messages.user_id_sender = %s and messages.user_id_receiver = %s))'''%(session["user_id"],user_id,user_id,session["user_id"]))
    return render_template('chat.html', user_id_receiver = user_id, messages = messages)


#выход пользователя 
def logout():
    #польностью очищает сессию
    session.clear()
    return redirect("/")


#регистрация
def regist():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']

        password = functions.hash_password(password)

        db_context.db_context('''INSERT INTO users (login, email, password)
        VALUES ('%s', '%s', '%s')
        '''%(login, email, password), commit=True)
    return render_template("regist.html")


#авторизация 
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        password = functions.hash_password(password)

        user = db_context.db_context("SELECT * FROM USERS WHERE login='%s' AND password='%s'"%(login, password))
        if user:
            if(user[0][3]==password):
                session["name"] = login
                session["user_id"] = user[0][0]
                return redirect("/")
    return render_template("auth.html")


#запрос на изменение пароля, отправка письма на почту
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        user = db_context.db_context("SELECT * FROM users WHERE email = '%s'"%(email))

        if user:
            token = functions.generate_random_number()  

            
            db_context.db_context("UPDATE users SET reset_token = '%s' WHERE email = '%s'"%(token, email), commit=True)

            link = url_for('reset', token=token)
            msg = Message('Восстановление пароля', sender = 'flask_first_app', recipients = [email])
            msg.body = f"Перейдите по ссылке чтобы восстановить пароль: http://localhost:5000{link}"
            mail.send(msg)

            return render_template("auth.html")
    return render_template("forgotpassword.html")


#изменение пароля
def reset(token):
    if request.method == 'POST':
        user = db_context.db_context("SELECT * FROM users WHERE reset_token = '%s'"%(token))

        password = request.form['new_password']
        password = functions.hash_password(password)

        db_context.db_context("UPDATE users SET password = '%s', reset_token = NULL WHERE id = '%s'"%(password, user[0][0]), commit=True)
        
        return redirect("/auth")
    return render_template("resetpassword.html")


#отправка сообщения и его добавление в БД
@socketio.on('send')
def handle_send(data):
    #текущее время
    curDT = datetime.now()
    time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    message = data['message']
    user_id_receiver = data['user_id_receiver']

    #file = data['file']
    #print('dgvsdgsgs', file)

    db_context.db_context('''
        INSERT INTO messages (user_id_sender, user_id_receiver, message_text, message_datetime)
        VALUES (%s, %s, '%s', '%s')
    '''%(session["user_id"], user_id_receiver, message, time),commit=True)

    socketio.emit('message', {'message': message, "sender" : session["name"], "time" : time})