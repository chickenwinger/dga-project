from flask import Flask
from .firebaseConfig import firebase

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
    
    return app