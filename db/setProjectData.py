import sys
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from .getProjectData import *
from .db import get_db

import pandas as pd

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
             data['radiusOuter'], data['length'], 50, user_id)
        )
        db.commit()
    except:
        print("setProjectInfoDB exception", file=sys.stdout)


def setProjectDateDB(name, date):
    project_id = getProjectIdDB(name)
    db = get_db()

    dates = db.execute(
        'select * from time_t where date=? and project_id=?', (date, project_id)).fetchall()
    if dates:
        return 
    try:
        db.execute(
            'insert or ignore into time_t (date,project_id) values(?,?)', (date, project_id))
        db.commit()
    except:
        print("setProjectDateDB exception", file=sys.stdout)


# def insertProjectSegmentDB(project_id, segments):
#     try:
#         db = get_db()
#         for segment in segments:
#             db.execute(
#                 "insert or ignore into segment_t (number,project_t) values(?,?)", (segment, project_id))
#         db.commit()
#     except:
#         print("insertProjectSegmentDataDB exception", file=sys.stdout)


# def insertProjectDiseaseDataDB(project_id, data):
#     db = get_db()
#     if isinstance(data, pd.core.frame.DataFrame):
#         insertProjectSegmentDB(project_id, data.loc['Ringnumber'])
#         segment_id = getProjectData.getProjectSegmentIdDB(
#             data.loc['Ringnumber'])
