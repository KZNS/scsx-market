from flask import Blueprint,render_template,url_for,session,redirect,g
from market.views.browse import browse
from market.models import db,MarketStaff

@browse.route("/")
def browse_home():
    this_staff = MarketStaff.query.filter(MarketStaff.id==g.id).first()
    return render_template('browse.html',this_staff=this_staff.todict())