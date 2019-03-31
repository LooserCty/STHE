import os
import sys
from matplotlib import pyplot as plt


import pandas as pd
from flask import (Blueprint, current_app, flash, g, json, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .project import bp
from .data import getPath


@bp.route('/getProjectDateAndType', methods=('GET', 'POST'))
def getProjectDateAndType():
    name = request.values.get('name')
    print(name, file=sys.stdout)

    d = getProjectData.getProjectDateDB(name)
    date = list(sorted(set(map(lambda x: x['date'], d))))
    type = ['综合评价', '裂缝长度', '裂缝宽度', '曲率变形', '错台', '沉降速率', '横向收敛变形', '渗漏水速率']
    data = {'date': date, 'type': type}

    return jsonify(data)


@bp.route('/getProjectSolutionShow', methods=('GET', 'POST'))
def getProjectSolutionShow():
    types = ['综合评价', '裂缝长度', '裂缝宽度', '曲率变形', '错台', '沉降速率', '横向收敛变形', '渗漏水速率']
    index = ['comprehensiveLevel', 'crackLength', 'crackWidth', 'radiusOfCurvature', 'segmentDislocation',
             'settlementRate', 'convergenceDeformation', 'leakageRate']
    d = dict(zip(types, index))

    name = request.values.get('name')
    date = request.values.get('date')
    type = request.values.get('type')

    path = '/static/data/'+g.user['username'] + '/' + \
        name + '/solution/image/'+date+'/'+d[type]+'.png'
    path = os.path.normpath(path)
    print(path)
    data = {'path': path}
    return jsonify(data)


@bp.route('/getProjectCurvePath', methods=('GET', 'POST'))
def getProjectCurvePath():
    name = request.values.get('name')

    d = getProjectData.getProjectDateDB(name)
    dates = list(map(lambda x: x['date'], d))
    dates.sort()

    path = getPath(name)+'solution/'
    scores = []
    for date in dates:
        fpath = path+date+'.csv'
        try:
            data = pd.read_csv(fpath, engine='python')
            s = data['comprehensiveValue'].mean()
            scores.append(s)
        except OSError:
            print('open solution csv except')

    # plot
    print('plot', dates, scores)
    fig = plt.figure()
    plt.plot(dates, scores, 'go-')
    plt.grid()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.xlabel('日期', fontsize=15)
    plt.ylabel('健康状态评分', fontsize=15)
    # plt.ylim(0, 100)
    plt.yticks((0, 25, 50, 75, 100))
    # plt.tick_params(labelsize=15)
    plt.tight_layout()

    cpath = path+'image/curve.png'
    fig.savefig(cpath)

    plt.close(fig)

    path = '/static/data/'+g.user['username'] + '/' + \
        name + '/solution/image/'+'curve.png'
    print(path)
    data = {'path': path}
    return jsonify(data)



