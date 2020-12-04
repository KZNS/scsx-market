from flask import Blueprint,redirect,url_for,g,abort
from market.models import db,MarketStaff
from market.interceptors import login_required
tests = Blueprint("test",__name__)

@tests.route("/hello")
def helo():
    return "world"

@tests.route('/admin')
@login_required
def makeadmin():
    print('Note: id=' + str(g.id) + ' is trying to change the level.')
    if MarketStaff.query.filter(MarketStaff.level=='admin').filter(MarketStaff.delete==False).limit(1).count() != 0:
        abort(404)
    this_user = MarketStaff.query.filter(MarketStaff.id==g.id).update({'level':'admin'})
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('index.helo'))

