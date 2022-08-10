from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from datetime import datetime, timezone

from money.controllers.auth import login_required
from money.db import get_db




bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    if request.method == 'POST':
        error = None
        amount = request.form['amount']
        category = request.form.get('category', None)
        if amount == '':
            error = True
            flash('Amount required', 'danger')
        if category == None:
            error = True
            flash('Category required', 'danger')
        if not error:
            db.execute(
                'INSERT INTO flows (amount, date, category, user) VALUES (?, CURRENT_TIMESTAMP, ?, ?)',
                (amount, category, g.user['id'])
            )
            db.commit()
            flash('Added Transaction', 'success')
            return redirect(url_for('index.index')) 

    categories = db.execute('SELECT * FROM categories').fetchall()
    sum_month = get_sum_month()
    sum_today = get_sum_day()
    return render_template('index/index.html', categories=categories, sum_month=sum_month, sum_today=sum_today)


def get_sum_month():
    db = get_db()
    sum = db.execute("SELECT SUM(amount) FROM flows WHERE user=? AND strftime('%m', flows.date)=strftime('%m', 'now')", [g.user['id']]).fetchone()[0]
    return sum or 0


def get_sum_day():
    db = get_db()
    sum = db.execute("SELECT SUM(amount) FROM flows WHERE user=? AND strftime('%Y %m %d', flows.date)=strftime('%Y %m %d', 'now')", [g.user['id']]).fetchone()[0]
    return sum or 0