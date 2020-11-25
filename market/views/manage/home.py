from market.views.manage import manage
from flask import render_template


@manage.route("/")
def manage_home():
    return render_template('manage.html')