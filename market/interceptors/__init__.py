from flask import request,redirect,current_app,abort,g
from functools import wraps
def admin_only(func):
    @wraps(func)
    def func_wrapper(*args,**kwargs):
        return func(*args,**kwargs)
    return func_wrapper

def login_required(func):
    @wraps(func)
    def func_wrapper(*args,**kwargs):
        return func(*args,**kwargs)
    return func_wrapper