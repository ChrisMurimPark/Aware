from app import db
from flask import g
from flask_login import login_required
from .models import User, Transaction, Category
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from functools import reduce
from collections import namedtuple


""" 
Spending by category last week, 30 days, 6 months, year
"""

# returns a map with categories as keys and named tuples as values. named tuple
# has total and percentage values. date range is based on input:
# 0 - last 7 days
# 1 - last 30 days
# 2 - last 3 months
# 3 - last 6 months
# 4 - last year
@login_required
def get_spending_by_category(date_range_id=0):
    end = datetime.today()
    start = end
    d = date_range_id
    if d is 0:
        start = end - timedelta(weeks=1)
    elif d is 1:
        start = end - timedelta(days=30)
    elif d is 2:
        start = end - relativedelta(months=+3)
    elif d is 3:
        start = end - relativedelta(months=+6)
    elif d is 4:
        start = end - relativedelta(years=+1)

    # construct a query to select cost gropued by category for user
    joined_table = db.session.query(Category).join(Category.transactions)
    with_cols = joined_table.add_columns(Category.user_id, Category.name, func.sum(Transaction.cost).label("cost"))
    with_filters = with_cols.filter_by(user_id = g.user.id).filter(Transaction.date.between(start, end))
    grouped = with_filters.group_by(Transaction.category_id)

    total_cost = reduce((lambda x, y: x + y), [entry.cost for entry in grouped])
    Stats = namedtuple('Stats', ['cost', 'percentage'])
    results = dict()
    for entry in grouped:
        results[entry.name] = Stats(entry.cost, entry.cost/total_cost)
    return results

