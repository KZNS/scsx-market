from flask import Blueprint, render_template, request, session, jsonify, abort
from market.models import MarketOrderDetail, MarketOrderMain, db
from market.utils import hash_password
from market.views.manage import manage


@manage.route("/orderinfo", methods=['GET', 'POST', 'PUT', 'DELETE'])
def order_home():
    if request.method == 'GET':
        suppliers = MarketOrderMain.query.filter(
            MarketOrderMain.delete != True).all()
        result = []
        for s in suppliers:
            result.append(s.todict())
        return jsonify(result)
    elif request.method == 'POST':
        if request.form.get('hiddenidinput') != '':
            print('-------')
            print(request.form.get('hiddenidinput'))
            id = int(request.form.get('hiddenidinput'))  # this is update
            update_dict = dict(request.form)
            update_dict.pop('hiddenidinput')
            print(update_dict)
            for k in update_dict:
                update_dict[k] = update_dict[k][0]
            print(update_dict)
            MarketOrderMain.query.filter(
                MarketOrderMain.id == id).update(update_dict)
            try:
                db.session.commit()
                return jsonify({"success": True})
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"success": False})
        _m = MarketOrderMain(
            order_id=request.form.get("order_id"),
            staff_id=request.form.get("staff_id"),
            gross_quantity=request.form.get('gross_quantity'),
            gross_price=request.form.get('gross_price'),
            time=request.form.get('time'),
            comment=request.form.get('comment')
        )
        db.session.add(_m)
        print('==========')
        try:
            db.session.commit()
            return jsonify({"success": True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success": False})
    elif request.method == 'DELETE':
        if not str(request.values.get('id')).isdigit():
            abort(400)
        id = int(request.values.get('id'))
        MarketOrderMain.query.filter(
            MarketOrderMain.id == id).update({'delete': True})
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success': False})
    elif request.method == 'PUT':
        pass
    else:
        abort(405)


@manage.route('/order')
def manage_order():
    return render_template('manage_order2.html')


'''
@manage.route("/order", methods=['POST', 'GET'])
def manage_order():
    if request.method == 'GET':
        orders = MarketOrderMain.query.filter_by(delete=False).limit(10).all()
        for i, order in enumerate(orders):
            details = MarketOrderDetail.query.filter_by(
                order_id=order.order_id, delete=False
            ).order_by(MarketOrderDetail.order_detail_id.asc()).all()
            orders[i].details = details
    else:
        if (request.values.get('order_id')):
            return "2333"
        else:
            return "wuwuwwu"
        if request.values.get('delete'):
            order_id = request.values.get('del_order_id')
            order = MarketOrderMain.query.filter_by(order_id=order_id).first()
            order.delete = True
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"success": False, "details": "fail"})

            details = MarketOrderDetail.query.filter_by(
                order_id=order_id, delete=False).all()
            for i in range(len(details)):
                details[i].delete = True
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"success": False, "details": "fail"})
        return "delete worked"

    return render_template('manage_order.html', title="订单管理", orders=orders)

'''


@manage.route("/order/add", methods=['POST', 'GET'])
def manage_order_add():
    if request.method == 'GET':
        return render_template('manage_order_add.html', title="添加订单")
    elif request.method == 'POST':
        print(request.values)
        order, details = get_order(request.values)
        db.session.add(order)
        for detail in details:
            db.session.add(detail)

        try:
            db.session.commit()
            return jsonify({"success": True, "data": "success"})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success": False, "details": "fail"})


@manage.route("/order/modify", methods=['POST'])
def manage_order_modify():
    if request.values.get('modify') == "true":
        order, details = get_order(request.values)

        return "mangae order modify"
    else:
        print(request.values.get('order_id'))
        order = MarketOrderMain.query.filter_by(
            order_id=request.values.get('order_id')
        )[0]
        details = MarketOrderDetail.query.filter_by(order_id=order.order_id)\
            .order_by(MarketOrderDetail.order_detail_id.asc()).all()
        order.details = details
        return render_template("manage_order_modify.html", title="修改订单", order=order)


def get_order(order_form):
    order = MarketOrderMain(
        order_id=order_form.get("order_id"),
        staff_id=order_form.get("staff_id"),
        gross_quantity=order_form.get('gross_quantity'),
        gross_price=order_form.get('gross_price'),
        time=order_form.get('time'),
        comment=order_form.get('comment')
    )

    order_id = order_form.get("order_id")
    order_detail_id = order_form.getlist("order_detail_id[]")
    merchandise_id = order_form.getlist("merchandise_id[]")
    merchandise_quantity = order_form.getlist("merchandise_quantity[]")
    unit_price = order_form.getlist("unit_price[]")
    detail_gross_price = order_form.getlist("detail_gross_price[]")
    detail_comment = order_form.getlist("detail_comment[]")
    details = []
    for i in range(len(order_detail_id)):
        print(i)
        detail = MarketOrderDetail(
            order_detail_id=order_detail_id[i],
            order_id=order_id,
            merchandise_id=merchandise_id[i],
            merchandise_quantity=merchandise_quantity[i],
            unit_price=unit_price[i],
            gross_price=detail_gross_price[i],
            comment=detail_comment[i]
        )
        details.append(detail)
    return order, details
