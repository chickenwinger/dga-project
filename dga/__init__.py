from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'abc123'
    
    from .authentication import authentication
    from .rtdatabase import rtdatabase
    
    app.register_blueprint(authentication, url_prefix='/')
    app.register_blueprint(rtdatabase, url_prefix='/')
    
    return app