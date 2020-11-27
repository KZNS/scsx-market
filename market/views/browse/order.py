from flask import Blueprint, url_for, render_template, request, session, jsonify, abort, redirect
from market.models import MarketOrderDetail, MarketOrderMain, db
from market.utils import hash_password, apply_query_filter
from market.views.browse import browse


@browse.route('/order', methods=['GET'])
def browse_order():
    args_dict = dict(request.values)
    orders = apply_query_filter(
        query_filter=args_dict,
        target_class=MarketOrderMain,
        target_query=MarketOrderMain.query.filter(MarketOrderMain.delete == False)
    ).all()
    details = apply_query_filter(
        args_dict,
        MarketOrderDetail,
        MarketOrderDetail.query.filter(MarketOrderDetail.delete == False),
    ).all()
    # MarketOrderMain.query.filter(MarketOrderMain.delete==False).all()
    #details = MarketOrderDetail.query.filter(MarketOrderDetail.delete == False).all()
    result = []
    details_result = []
    for i, order in enumerate(orders):
        this_order = {}
        this_order['main'] = order
        this_order['details'] = []
        for detail in details:
            if detail.order_id == order.order_id:
                this_order['details'].append(detail)
        result.append(this_order)
    return render_template('browse_order2.html', result=result, title="订单查询")

