from flask import Blueprint,render_template,request,session,jsonify
from market.models import db,MarketStaff
from market.utils import hash_password
order = Blueprint("order",__name__,template_folder='templates',static_folder='static')

@order.route("/manage/order")
def manage_order():
    return render_template('manage_order.html')