from flask import Blueprint,render_template,url_for,session,redirect,g
from market.interceptors import login_required
from market.views.browse import browse


@browse.route("/")
def browse_home():
    return render_template('browse.html',id=g.id,level=g.level)