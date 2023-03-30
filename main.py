from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
import mail_config

app = Flask(__name__,
    static_url_path='', 
    static_folder='static',
)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = "files2"
Session(app)

from engineio.payload import Payload

Payload.max_decode_packets = 500
socketio = SocketIO(app, max_http_buffer_size=10000000)

mail_config.mail_config(app)
mail = mail_config.mail_set(app)

import views


# код страничек находится в файле views
app.add_url_rule('/', view_func=views.welcome)

app.add_url_rule('/chat/<user_id>', view_func=views.chat, methods=["POST","GET"])

app.add_url_rule('/logout', view_func=views.logout)

app.add_url_rule('/regist', view_func=views.regist, methods=["POST","GET"])

app.add_url_rule('/auth', view_func=views.auth, methods=["POST","GET"])

app.add_url_rule('/forgot_password', view_func=views.forgot, methods=["POST","GET"])

app.add_url_rule('/reset_password/<token>', view_func=views.reset, methods=["POST","GET"])

app.add_url_rule('/files', view_func=views.files, methods=["POST","GET"])

if __name__ == '__main__':
    socketio.run(app, host='192.168.43.218', port=5000)