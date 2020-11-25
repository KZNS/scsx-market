from flask import Blueprint, render_template, request, session, jsonify
from market.models import MarketOrderDetail, MarketOrderMain, db
from market.utils import hash_password

order = Blueprint("order", __name__,
                  template_folder='templates', static_folder='static')


@order.route("/manage/order", methods=['POST', 'GET'])
def manage_order():
    if request.method == 'GET':
        orders = MarketOrderMain.query.limit(10).all()
    else:
        orders = 100

    return render_template('manage_order.html', result = orders)


@order.route("/manage/order/add", methods=['POST', 'GET'])
def manage_order_add():
    if request.method == 'GET':
        return render_template('manage_order_add.html')
    elif request.method == 'POST':
        print(request.values)
        _u = MarketOrderMain(
            order_id=request.values.get("order_id"),
            staff_id=request.values.get("staff_id"),
            gross_quantity=request.values.get('gross_quantity'),
            gross_price=request.values.get('gross_price'),
            time=request.values.get('time'),
            comment=request.values.get('comment')
        )
        db.session.add(_u)

        order_id            = request.values.get("order_id")
        order_detail_id     = request.values.getlist("order_detail_id[]")
        merchandise_id      = request.values.getlist("merchandise_id[]")
        merchandise_quantity= request.values.getlist("merchandise_quantity[]")
        unit_price          = request.values.getlist("unit_price[]")
        detail_gross_price  = request.values.getlist("detail_gross_price[]")
        detail_comment      = request.values.getlist("detail_comment[]")
        print(order_detail_id)
        print(order_detail_id[0])
        print(merchandise_quantity[0])
        for i in range(len(order_detail_id)):
            print(i)
            _u = MarketOrderDetail(
                order_detail_id=order_detail_id[i],
                order_id=order_id,
                merchandise_id=merchandise_id[i],
                merchandise_quantity=merchandise_quantity[i],
                unit_price=unit_price[i],
                gross_price=detail_gross_price[i],
                comment=detail_comment[i]
            )
            db.session.add(_u)

        try:
            db.session.commit()
            return jsonify({"success": True, "data": "success"})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success": False, "details": "fail"})


@order.route("/manage/order/modify")
def manage_order_modify():
    return "mangae order modify"
