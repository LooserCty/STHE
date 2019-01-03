import sys

from flask import (Blueprint, flash, g, json, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.exceptions import abort

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .analysis import analysisRealize
from .data import dataRealize
from .solution import solutionRealize

bp = Blueprint('project', __name__, url_prefix='/project')


@bp.route('/')
@login_required
def index():
    projects = getProjectData.getAllProjectInfoDB()
    for project in projects:
        for d in project.keys():
            print(d, file=sys.stdout)
    return render_template('project/index.html', projects=projects)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        print(request.form, file=sys.stdout)
        data = request.form
        setProjectData.setProjectInfoDB(data)
        return redirect(url_for('project.index'))

    return render_template('project/create.html')


@bp.route('/data', methods=('GET', 'POST'))
@login_required
def data():
    return dataRealize()


@bp.route('/analysis', methods=('GET', 'POST'))
@login_required
def analysis():
    return analysisRealize()


@bp.route('/solution', methods=('GET', 'POST'))
@login_required
def solution():
    return solutionRealize()


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user_t u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
