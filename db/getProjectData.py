from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from .db import get_db


def getUserDB(username):
    db = get_db()

    user = db.execute(
        'select * from user_t where username=?', (username,)
    ).fetchone()

    return user

def getProjectIdDB(name):
    db = get_db()
    user_id = session['user_id']

    id = db.execute(
        'select id from project_t where name=? and user_id=?', (name, user_id)
    ).fetchone()

    return id


def getProjectInfoDB(name):
    db = get_db()
    user_id = session['user_id']

    project = db.execute(
        'select * from project_t where name=? and user_id=?', (name, user_id)
    ).fetchone()

    return project

def getAllProjectInfoDB():
    db = get_db()
    user_id = session['user_id']

    projects = db.execute(
        'select name,describe,depth,radiusInside,radiusOuter,length,strength from project_t where user_id=?', (
            user_id,)
    ).fetchall()

    return projects
