import sys

import pandas as pd
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from ..db import getProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .data import getPath, getPathRel


def score2Level(s):
    l = 1
    if s > 75:
        l = 4
    elif s > 50:
        l = 3
    elif s > 25:
        l = 2
    else:
        l = 1
    return l


def getAllSolutionData(name):
    path = getPath(name)+'solution/'
    rpath = getPathRel(name)+'solution/'
    dataTable = []

    d = getProjectData.getProjectDateDB(name)
    dates = sorted(set(map(lambda x: x['date'], d)))
    for i,date in enumerate(dates):
        # date = dates[i-1]
        row = [i, date]
        fpath = path+date+'.csv'
        try:
            data = pd.read_csv(fpath, engine='python')
            s = data['comprehensiveValue'].mean()
            s=int(s*100)/100
            l = score2Level(s)
            downloadPath = rpath+date+'.csv'
            dateurl = url_for('project.solutionDateData', name=name, date=date)
            row.extend([s, l, downloadPath, dateurl])
            dataTable.append(row)
        except:
            print('open solution csv except')

    return dataTable


def getSolutionDateData(name, date):
    # path = getPathRel(name)+'solution/'+date+'.csv'
    path = getPath(name)+'solution/'+date+'.csv'
    try:
        data = pd.read_csv(path, engine='python')
    except:
        print('open solution csv except')
    return data


def getReportData(name):
    path = getPath(name)+'solution/'
    rpath = getPathRel(name)+'solution/'
    dataTable = []

    d = getProjectData.getProjectDateDB(name)
    dates = list(map(lambda x: x['date'], d))
    for i in range(1, len(dates)+1):
        date = dates[i-1]
        row = [i, date]
        fpath = path+date+'.csv'
        try:
            data = pd.read_csv(fpath, engine='python')
            s = data['comprehensiveValue'].mean()
            l = score2Level(s)
            downloadPath = rpath+date+'.csv'
            dateurl = url_for('project.solutionDateData', name=name, date=date)
            row.extend([s, l, downloadPath, dateurl])
            dataTable.append(row)
        except:
            print('open solution csv except')

    return dataTable


def solutionRealize():
    # mode：'1'为评价结果, '2'为评价数据,'3'为分析报告,'4'为评价变化曲线
    name = request.values.get('name')
    mode = request.values.get('mode')
    datas = {}
    datas['name'] = name
    print(request.values, file=sys.stdout)
    if request.method == 'POST':
        if mode == '1':
            return redirect(url_for('project.solution', name=name, mode=1))
        elif mode == '2':
            return redirect(url_for('project.solution', name=name, mode=2))
        elif mode == '3':
            return redirect(url_for('project.solution', name=name, mode=3))
        else:
            return redirect(url_for('project.solution', name=name, mode=4))
    else:
        if mode == '1':
            return render_template('project/solution/solutionShow.html', datas=datas)
        elif mode == '2':
            data = getAllSolutionData(name)
            datas['data'] = data
            return render_template('project/solution/solutionData.html', datas=datas)
        elif mode == '3':
            return render_template('project/solution/solutionCurve.html', datas=datas)
        else:
            data = getReportData(name)
            datas['data'] = data
            return render_template('project/solution/solutionReport.html', datas=datas)


def solutionDateDataRealize():
    name = request.values.get('name')
    date = request.values.get('date')
    datas = {}
    datas['name'] = name
    datas['date'] = date
    print(request.values, file=sys.stdout)
    if request.method == 'POST':
        return redirect(url_for('project.solutionDateData', name=name, date=date))
    else:
        data = getSolutionDateData(name, date)
        datas['data'] = data.T
        return render_template('project/solution/solutionDateData.html', datas=datas)
