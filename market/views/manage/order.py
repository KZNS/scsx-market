from flask import Blueprint, render_template, request, session, jsonify
from market.models import db, MarketStaff
from market.utils import hash_password
import json
from market.views.manage import manage

@manage.route("/order", methods=['POST', 'GET'])
def manage_order():
    return render_template('manage_order.html')


@manage.route("/order/add", methods=['POST', 'GET'])
def manage_order_add():
    if request.method == 'GET':
        return render_template('manage_order_add.html')
    elif request.method == 'POST':
        jsoninput = request.form
        print(jsoninput)
        for i in jsoninput:
            print(i)
        return '2333'
        _u = MarketStaff(
            staff_id=jsoninput['staff_id'],
            gross_price=jsoninput['gross_price'],
            gross_quantity=jsoninput['gross_quantity']
        )
        db.session.add(_u)
        try:
            db.session.commit()
            return jsonify({"success": True, "data": "success"})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success": False, "details": "fail"})
    return "mangae order add"


@manage.route("/order/modify")
def manage_order_modify():
    return "mangae order modify"
