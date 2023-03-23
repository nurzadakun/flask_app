from flask_mail import Mail

def mail_config(app):
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'nurzada670@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wxtcbdbyciknjgqt'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

def mail_set(app):
    mail = Mail(app)
    return mail