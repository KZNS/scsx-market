from flask import Blueprint, render_template, request, url_for, flash, redirect
from market.models import MarketStaff, db
staff = Blueprint("staff", __name__,
                  template_folder='templates', static_folder='static')


@staff.route("/staff")
def staff_query():
    id = request.values.get('id')
    name = request.values.get('name')
    level = request.values.get('level')
    telephone = request.values.get('telephone')
    salary = request.values.get('salary')

    data = MarketStaff.query.filter(MarketStaff.delete == False)

    if (id):
        data = data.filter(MarketStaff.id.like('%%' + str(id) + '%%'))
    if (name):
        data = data.filter(MarketStaff.name.like('%%' + name + '%%'))
    if (level):
        data = data.filter(MarketStaff.level.like('%%' + level + '%%'))
    if (telephone):
        data = data.filter(MarketStaff.telephone.like('%%' + telephone + '%%'))
    if (salary):
        data = data.filter(MarketStaff.salary.like('%%' + salary + '%%'))

    return render_template('staff.html', data=data)
