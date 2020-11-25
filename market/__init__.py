import os
import socket
from flask import Flask, request, session
from flask_session import Session
from redis import Redis
from market.views import tests as testapp
from market.views import index as indexapp
from market.views import user as userapp
from market.views import staff as staffapp
from market.views import browse as browseapp
from market.views import manage as manageapp
from market.views import order as orderapp
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
            app.config['SERVER_NAME'] = 'www.dutbit.com'
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
            app.config['SUBDOMAINS'] = subdomains['PRODUCTION']
            app.config['SESSION_TYPE'] = 'redis'
            app.config['SESSION_REDIS'] = Redis(
                host='localhost',port=6379
            )
            if 'mysql+pymysql' not in app.config['SQLALCHEMY_DATABASE_URI']:
                raise EnvironmentError("No db connection uri provided")
                exit(-1)
        else:
            print('------ starting service in development ------')
            app.config['DEBUG'] = True
            app.config['SERVER_NAME'] = '127.0.0.1:5000'
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
            app.config['SUBDOMAINS'] = subdomains['DEVELOPMENT']
            app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SESSION_USE_SIGNER'] = True
        app.config['SESSION_PERMANENT'] = True  #sessons是否长期有效，false，则关闭浏览器，session失效
        app.config['PERMANENT_SESSION_LIFETIME'] = 3600   #session长期有效，则设定session生命周期，整数秒，默认大概不到3小时。
        Session(app)
        db.init_app(app)
        #db.drop_all()
        db.create_all()
        app.register_blueprint(testapp)
        app.register_blueprint(indexapp)
        app.register_blueprint(userapp)
        app.register_blueprint(staffapp)
        app.register_blueprint(manageapp)
        app.register_blueprint(browseapp)
        app.register_blueprint(orderapp)
        #app.config['SERVER_NAME'] = 'dutbit.com'
        app.config['SECRET_KEY'] = 'Do not go gentle into that good night'
        return app
