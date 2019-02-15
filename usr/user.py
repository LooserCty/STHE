import sys
import functools
import os

from flask import (Blueprint, flash, g, redirect, render_template, request, json, jsonify,
                   session, url_for, current_app)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


def createUserDir(username):
    print(current_app.static_folder, file=sys.stdout)
    try:
        os.makedirs(current_app.static_folder+'/data/'+username)
    except OSError:
        pass


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user_t WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            createUserDir(username)
            
            db.execute(
                'INSERT INTO user_t (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('user.login'))

        flash(error)

    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user_t WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('project.index'))

        flash(error)

    return render_template('user/login.html')


# !!!!!!!!!!!!!!!!
# 确保每次请求被刷新的g中仍有用户信息，session不会刷新为啥不直接使用？因为信息安全？
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user_t WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view
