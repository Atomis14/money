from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from money.controllers.auth import login_required
from money.db import get_db

bp = Blueprint('flow', __name__, url_prefix='/flow')

@bp.route('/')
@login_required
def flow():
    db = get_db()        
    transactions = db.execute(
        "SELECT * FROM flows JOIN categories ON flows.category=categories.id WHERE flows.user=? ORDER BY id DESC",
        [g.user['id']]
    ).fetchall()
    return render_template('flow/index.html', transactions=transactions)


@bp.route('/delete/<int:id>')
@login_required
def flow_delete(id):
    db = get_db()
    cur = db.execute("DELETE FROM flows WHERE id=? AND user=?", [id, g.user['id']])
    db.commit()
    if cur.rowcount:
        flash('Transaction deleted', 'success')
    else:
        flash('Could not delete transaction', 'danger')
    return redirect(url_for('flow.flow'))