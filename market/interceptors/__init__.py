from flask import request,redirect,current_app,abort,g,session,url_for
from functools import wraps


def admin_only(func):
    @wraps(func)
    def func_wrapper(*args,**kwargs):
        if session.get('id') is None:
            return redirect(url_for('index.helo'))
        if g.level != 'admin':
            return redirect(url_for('browse.browse_home'))
        return func(*args,**kwargs)
    return func_wrapper
    

def login_required(func):
    @wraps(func)
    def func_wrapper(*args,**kwargs):
        if session.get('id') is None:
            return redirect(url_for('index.helo'))
        g.id = session['id']
        g.level = session['level']
        return func(*args,**kwargs)
    return func_wrapper