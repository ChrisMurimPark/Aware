from flask import flash

from .models import Transaction, Category
from .aware_utils import commit_db

from io import StringIO
from datetime import datetime
import csv


def process_data(d, session, user):
    # parse file
    with StringIO(d.read().decode('utf-8')) as f:
        reader = csv.reader(f)
        header = next(reader)
        indices = process_header(header)
        if indices is None:
            return
        categories = [c.name for c in user.categories.all()]
        for line in reader:
            date = datetime.strptime(line[indices[0]], '%m/%d/%Y').date()
            name = line[indices[1]]
            amount = float(line[indices[2]])
            transaction_type = line[indices[3]]
            category = line[indices[4]]
            # does not handle credits
            if transaction_type == 'credit':
                continue
            process_category(category, categories, session, user)
            process_transaction(category, name, date, amount, session, user.id)
        if not commit_db(session):
            flash('Something went wrong while uploading the data.')
        else:
            flash('Successfully imported data!')


def process_header(h):
    try:
        REQ_COLS = ['Date', 'Description', 'Amount', 'Transaction Type', 'Category']
        indices = [h.index(c) for c in REQ_COLS]
        return indices
    except ValueError:
        flash('The file requires columns named {}'.format(', '.join(REQ_COLS)))
        return None


def process_category(c, categories, session, user):
    if c not in categories:
        session.add(Category(name=c, user=user))
        categories.append(c)


def process_transaction(cat, name, date, amt, session, u_id):
    cat_results = session.query(Category).filter_by(name=cat, user_id=u_id)
    cat_id = cat_results.first().id
    t = Transaction(name=name, date=date, category_id=cat_id, cost=amt, user_id=u_id)
    session.add(t)

