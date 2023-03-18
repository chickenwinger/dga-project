from flask import Flask
from flask_mail import Mail
from .firebaseConfig import firebase
import os

# for authentication
auth = firebase.auth()
# for firebase realtime database
db = firebase.database()
# for firebase storage but we will not use it in this app
# storage = firebase.storage()

def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'abc123'
    
    from .authentication import authentication
    from .rtdatabase import rtdatabase
    
    app.register_blueprint(authentication, url_prefix='/')
    app.register_blueprint(rtdatabase, url_prefix='/')

    app.config['DEBUG'] = True
    # app.config['TESTING'] = True
    app.config['MAIL_SERVER']='smtp-relay.sendinblue.com ' # smtp relay server, can be found at https://support.google.com/a/answer/176600?hl=en
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@sendinblue.com'
    app.config['MAIL_MAX_EMAILS'] = None
    # app.config['MAIL_SUPPRESS_SEND'] = False
    app.config['MAIL_ASCII_ATTACHMENTS'] = False

    mail = Mail(app)
    
    return app