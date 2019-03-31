import os
import sys

import pandas as pd
from flask import (Blueprint, current_app, flash, g, json, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.exceptions import abort

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .analysis import analysisRealize
from .data import dataRealize, dataDateDataRealize
from .solution import solutionDateDataRealize, solutionRealize

bp = Blueprint('project', __name__, url_prefix='/project')


def createProjectDirs(name):
    try:
        path = current_app.static_folder + \
            '/data/'+g.user['username']+'/'+name+'/'
        disease = path+'disease'
        image = path+'solution/image'
        tmp = path+'tmp'
        os.makedirs(disease)
        os.makedirs(image)
        os.makedirs(tmp)
    except OSError:
        pass


@bp.route('/')
@login_required
def index():
    projects = getProjectData.getAllProjectInfoDB()
    # for project in projects:
    #     print(project)
    #     for d in project.keys():
    #         print(d, file=sys.stdout)
    return render_template('project/index.html', projects=projects)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        data = request.values
        print(request.values, file=sys.stdout)
        createProjectDirs(data['name'])
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


@bp.route('/dataDateData', methods=('GET', 'POST'))
@login_required
def dataDateData():
    return dataDateDataRealize()


@bp.route('/solutionDateData', methods=('GET', 'POST'))
@login_required
def solutionDateData():
    return solutionDateDataRealize()
