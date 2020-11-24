from flask import Blueprint,render_template,url_for,session,redirect,g
from market.interceptors import admin_only,login_required
manage = Blueprint("manage",__name__,template_folder='templates',static_folder='static')

@manage.before_request
@login_required
@admin_only
def before_bp():
    pass

@manage.route("/manage")
def manage_home():
    return render_template('manage.html')