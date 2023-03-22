from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from flask_socketio import SocketIO
import db_context, mail_config, functions
from datetime import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

mail_config.mail_config(app)
mail = mail_config.mail_set(app)

@app.route("/")
def welcome():
    if not session.get("name"):
        return render_template('index.html')
    users = db_context.db_context("Select * from users where users.login <> '%s'"%session["name"])
    return render_template('profile.html', login=session["name"], users = users)

@app.route('/chat/<user_id>')
def chat(user_id):
    if not session.get("name"):
        return render_template('index.html')
    #messages = db_context.db_context('''Select * from messages 
     #   where (messages.user_id_sender = %s and messages.user_id_receiver = %s)
      #  or (messages.user_id_sender = %s and messages.user_id_receiver = %s)'''%(session["user_id"],user_id,user_id,session["user_id"]))
    
    messages = db_context.db_context('''Select users.login, messages.message_text, messages.message_datetime from users, messages 
        where users.id=messages.user_id_sender and ((messages.user_id_sender = %s and messages.user_id_receiver = %s)
        or (messages.user_id_sender = %s and messages.user_id_receiver = %s))'''%(session["user_id"],user_id,user_id,session["user_id"]))

    print(messages)
    return render_template('chat.html', user_id_receiver = user_id, messages = messages)

#выход
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#авторизация
@app.route("/auth", methods=['GET','POST'])
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

@socketio.on('send')
def handle_send(data):
    curDT = datetime.now()
    time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    message = data['message']
    user_id_receiver = data['user_id_receiver']
    db_context.db_context('''
        INSERT INTO messages (user_id_sender, user_id_receiver, message_text, message_datetime)
        VALUES (%s, %s, '%s', '%s')
    '''%(session["user_id"], user_id_receiver, message, time),commit=True)
    print('ffffff', message)
    socketio.emit('message', {'message': message, "sender" : session["name"], "time" : time})

if __name__ == '__main__':
    socketio.run(app)