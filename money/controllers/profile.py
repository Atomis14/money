from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from money.controllers.auth import login_required
from money.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
  if request.method == 'POST':
    current = request.form['current_password']
    new1 = request.form['new_password']
    new2 = request.form['new_password_2']
    error = False
    if not check_password_hash(g.user['password'], current):
      error = True
      flash('Current password was not correct', 'danger')
    if new1 != new2:
      error = True
      flash('Passwords are not the same', 'danger')
    if new1 == '':
      error = True
      flash('Password cannot be empty', 'danger')
    if not error:
      flash('Password changed', 'success')
  return render_template('profile/index.html')


@bp.route('/delete/<string:type>', methods=['GET', 'POST'])
@login_required
def profile_delete(type):
  if type not in ('data', 'profile'):
    return redirect(url_for('profile.profile'))
  if request.method == 'POST':
    db = get_db()
    confirmation = request.form.get('confirmation', None)
    if confirmation:
      if type == 'data':
        db.execute("DELETE FROM flows WHERE user=?", [g.user['id']])
        db.commit()
        flash('Your data was deleted successfully', 'success')
        return redirect(url_for('profile.profile'))
      elif type == 'profile':
        db.execute("DELETE FROM users WHERE id=?", [g.user['id']])
        db.commit()
        flash('Your account was deleted successfully', 'success')
        return redirect(url_for('auth.logout'))
    else:
      flash('Please confirm the deletion', 'danger')
  return render_template('profile/delete.html', type=type)