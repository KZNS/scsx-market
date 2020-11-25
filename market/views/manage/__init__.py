from flask import Blueprint,render_template,url_for,session,redirect,g
from market.interceptors import admin_only,login_required
manage = Blueprint("manage",__name__,template_folder='templates',static_folder='static',url_prefix='/manage')
from market.views.manage import home,staff,order,supplyer


@manage.before_request
@login_required
@admin_only
def before_bp():
    pass
