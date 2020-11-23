import os
import socket
from flask import Flask, Request
from .test import tests as testapp

subdomains = {
    'DEVELOPMENT':{
        'www':'',
        'files':'',
    },
    'PRODUCTION':{
        'www':'www',
        'files':'files',
    }
}


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

def create_app():
    app = Flask(__name__)
    with app.app_context():
        from market.models import db
        if ip == '172.31.240.127':  # is dutbit.com
            print('------ starting service in production ------')
            app.config['DEBUG'] = False
            app.config['SERVER_NAME'] = 'dutbit.com'
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
            app.config['SUBDOMAINS'] = subdomains['PRODUCTION']
            if 'mysql+pymysql' not in app.config['SQLALCHEMY_DATABASE_URI']:
                raise EnvironmentError("No db connection uri provided")
                exit(-1)
        else:
            print('------ starting service in development ------')
            app.config['DEBUG'] = True
            app.config['SERVER_NAME'] = '127.0.0.1:5000'
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
            app.config['SUBDOMAINS'] = subdomains['DEVELOPMENT']

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        # db.drop_all()
        db.create_all()
        app.register_blueprint(testapp)
        #app.config['SERVER_NAME'] = 'dutbit.com'
        app.config['SECRET_KEY'] = 'Do not go gentle into that good night'
        return app
