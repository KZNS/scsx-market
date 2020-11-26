from market.views.manage import manage
from flask import render_template,g
from market.models import db,MarketStaff

@manage.route("/")
def manage_home():
    this_staff = MarketStaff.query.filter(MarketStaff.id==g.id).first()
    return render_template('manage.html',this_staff=this_staff.todict())