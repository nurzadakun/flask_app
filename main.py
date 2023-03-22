from flask import Flask, render_template, session
from flask_session import Session
from flask_socketio import SocketIO
import db_context, mail_config
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