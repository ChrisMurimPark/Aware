from app import db
from flask import g
from flask_login import login_required
from .models import User, Transaction, Category
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from functools import reduce
from collections import namedtuple


""" 
Spending by category last week, 30 days, 6 months, year
"""

# returns a map with categories as keys and named tuples as values. named tuple
# has total and percentage values. between start and end dates.
@login_required
def get_spending_by_category(start, end):
    # construct a query to select cost gropued by category for user
    joined_table = db.session.query(Category).join(Category.transactions)
    with_cols = joined_table.add_columns(Category.user_id, Category.name, func.sum(Transaction.cost).label("cost"))
    with_filters = with_cols.filter_by(user_id = g.user.id).filter(Transaction.date.between(start, end))
    grouped = with_filters.group_by(Transaction.category_id)
    final = grouped.order_by(func.sum(Transaction.cost).desc())
    return [[entry.name, entry.cost] for entry in final]
    
@login_required
def get_total_spending(start, end):
    return db.session.query(func.sum(Transaction.cost).label("total_cost")).filter(Transaction.date.between(start, end)).first()[0]

