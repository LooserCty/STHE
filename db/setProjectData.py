import sys
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from .db import get_db


bp = Blueprint('getData', __name__, url_prefix='/getData')


def setProjectInfoDB(data):
    db = get_db()
    user_id = session['user_id']
    print(data, file=sys.stdout)
    try:
        db.execute(
            'INSERT OR IGNORE INTO project_t (name, describe, depth, radiusInside, radiusOuter, length, strength, user_id) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (data['name'], data['describe'], data['depth'], data['radiusInside'],
             data['radiusOuter'], data['length'], data['strength'], user_id)
        )
        db.commit()
    except:
        pass
