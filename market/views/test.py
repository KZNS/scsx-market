from flask import Blueprint,redirect,url_for,g
from market.models import db,MarketStaff
from market.interceptors import login_required
tests = Blueprint("test",__name__)

@tests.route("/hello")
def helo():
    return "world"

@tests.route('/admin')
@login_required
def makeadmin():
    this_user = MarketStaff.query.filter(MarketStaff.id==g.id).update({'level':'admin'})
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('index.helo'))

