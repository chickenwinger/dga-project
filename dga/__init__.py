from flask import Flask
from flask_mail import Mail
from .firebaseConfig import firebase
import os

from config import Config

# for authentication
auth = firebase.auth()
# for firebase realtime database
db = firebase.database()
# for firebase storage but we will not use it in this app
# storage = firebase.storage()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    with app.app_context():
        from .authentication import authentication
        from .rtdatabase import rtdatabase
        from .graph import graph

        app.register_blueprint(authentication, url_prefix='/')
        app.register_blueprint(rtdatabase, url_prefix='/')
        app.register_blueprint(graph, url_prefix='/')
        
        mail = Mail()
        mail.init_app(app)
    
        return app