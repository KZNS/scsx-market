from flask import Blueprint, render_template, request, url_for, flash, redirect
from market.models import MarketStaff, db
staff = Blueprint("staff", __name__,
                  template_folder='templates', static_folder='static')


@staff.route("/staff", methods=['GET'])
def staff_query():
    staff_id = request.values.get('staff_id')
    name = request.values.get('name')
    level = request.values.get('level')
    telephone = request.values.get('telephone')
    salary = request.values.get('salary')
    comment = request.values.get('comment')

    data = MarketStaff.query.filter(MarketStaff.delete == False)

    if (staff_id):
        data = data.filter(MarketStaff.staff_id.like('%%' + staff_id + '%%'))
    if (name):
        data = data.filter(MarketStaff.name.like('%%' + name + '%%'))
    if (level):
        data = data.filter(MarketStaff.level.like('%%' + level + '%%'))
    if (telephone):
        data = data.filter(MarketStaff.telephone.like('%%' + telephone + '%%'))
    if (salary):
        data = data.filter(MarketStaff.salary.like('%%' + salary + '%%'))
    if (comment):
        data = data.filter(MarketStaff.comment.like('%%' + comment + '%%'))

    return render_template('staff.html', data=data)


@staff.route("/staff/del/<int:id>", methods=['DELETE'])
def delete(id):
    MarketStaff.query.filter(MarketStaff.id == id).update({'delete': True})
    try:
        db.session.commit()
        return 'succeed'
    except Exception as e:
        print(e)
        db.session.rollback()
        return 'fail'
