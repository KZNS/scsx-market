from flask import Blueprint,render_template,url_for,session,redirect,g
from market.interceptors import login_required
browse = Blueprint("browse",__name__,template_folder='templates',static_folder='static')

@browse.before_request
@login_required
def before_bp():
    pass


@browse.route("/browse")
@login_required
def browse_home():
    return render_template('browse.html',id=g.id,level=g.level)