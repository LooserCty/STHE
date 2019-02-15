import os
import sys

import pandas as pd
from flask import (Blueprint, current_app, flash, g, json, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .project import bp


@bp.route('/getProjectDate', methods=('GET', 'POST'))
def getProjectDate():
    name = request.values.get('name')
    print(name, file=sys.stdout)
    date = ['1998/12/12', '2011/9/8', '2017/6/8']
    type = ['综合评价', '裂缝长度', '裂缝宽度', '曲率变形', '错台', '沉降速率', '横向收敛变形', '渗漏水速率']
    data = {'date': date, 'type': type}
    return jsonify(data)


@bp.route('/getProjectSolutionShow', methods=('GET', 'POST'))
def getProjectSolutionShow():
    name = request.values.get('name')
    date = request.values.get('date')
    type = request.values.get('type')
    print(request.values, file=sys.stdout)
    data = {}
    return jsonify(data)
