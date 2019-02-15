import sys

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.exceptions import abort

from .db import get_db


def getUserDB(username):
    db = get_db()

    user = db.execute(
        'select * from user_t where username=?', (username,)
    ).fetchone()

    print('db user:', user, file=sys.stdout)
    return user


def getProjectIdDB(name):
    db = get_db()
    user_id = session['user_id']

    id = db.execute(
        'select id from project_t where name=? and user_id=?', (name, user_id)
    ).fetchone()

    print('db project_id:', id, file=sys.stdout)
    return id


# def getProjectInfoDB(name):
#     db = get_db()
#     user_id = session['user_id']

#     project = db.execute(
#         'select * from project_t where name=? and user_id=?', (name, user_id)
#     ).fetchone()

#     return project

def getAllProjectInfoDB():
    db = get_db()
    user_id = session['user_id']

    projects = db.execute(
        'select name,describe,depth,radiusInside,radiusOuter,length,strength from project_t where user_id=?', (
            user_id,)
    ).fetchall()

    print('db projects:', projects, file=sys.stdout)
    return projects


def getProjectDateDB(name):
    project_id = getProjectIdDB(name)
    db = get_db()

    dates = db.execute(
        'select date from time_t where project_id=?', (project_id,)).fetchall()

    print('db project dates:', dates, file=sys.stdout)
    return dates
