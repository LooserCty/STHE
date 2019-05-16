import sys

import numpy as np
import pandas as pd
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from ..db import getProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .data import getPath, getPathRel
from .analysis import level2Roman


def score2Level(s):
    l = 4
    if s > 75:
        l = 1
    elif s > 50:
        l = 2
    elif s > 25:
        l = 3
    return l


def quduanScore(v):
    n = v.shape[0]
    w = np.array([1/n]*n)
    d = ((n+1)/2)**(4-4*v/100)
    vw = w*d/(w*d).sum()
    return (v*vw).sum()


def getAllSolutionData(name):
    path = getPath(name)+'solution/'
    rpath = getPathRel(name)+'solution/'
    dataTable = []

    d = getProjectData.getProjectDateDB(name)
    dates = sorted(set(map(lambda x: x['date'], d)))
    for i, date in enumerate(dates):
        # date = dates[i-1]
        row = [i, date]
        fpath = path+date+'.csv'
        try:
            data = pd.read_csv(fpath, engine='python', encoding='utf8')
            s = quduanScore(data['comprehensiveValue'])
            s = int(s*100)/100
            l = score2Level(s)
            l = level2Roman(l)
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
        data = pd.read_csv(path, engine='python', encoding='utf8')
        ixs = ['crackLengthScore', 'crackWidthScore', 'radiusOfCurvatureScore',
               'segmentDislocationScore', 'settlementRateScore', 'convergenceDeformationScore', 'leakageRateScore']
        for ix in ixs:
            data.pop(ix)
        data = data.applymap(level2Roman)
    except:
        print('open solution csv except')
    return data


def getQuduanScore(data):
    s = quduanScore(data)
    s = int(s*100)/100
    return s


def getReportData(name):
    path = getPath(name)+'solution/'
    # rpath = getPathRel(name)+'solution/'
    dataTable = []

    d = getProjectData.getProjectDateDB(name)
    dates = sorted(set(map(lambda x: x['date'], d)))
    for date in dates:
        row = [date]
        fpath = path+date+'.csv'
        try:
            data = pd.read_csv(fpath, engine='python', encoding='utf8')

            s = getQuduanScore(data['comprehensiveValue'])
            level = score2Level(s)
            lroman = level2Roman(level)
            row.extend([s, lroman])

            ixs = ['crackLengthScore', 'crackWidthScore', 'radiusOfCurvatureScore',
                   'segmentDislocationScore', 'settlementRateScore', 'convergenceDeformationScore', 'leakageRateScore']
            diseaseS = np.array([])
            for ix in ixs:
                s = getQuduanScore(data[ix])
                diseaseS = np.append(diseaseS, s)
            minIx = diseaseS.argmin()
            mainDisease = {
                0: '裂缝长度',
                1: '裂缝宽度',
                2: '曲率半径',
                3: '错台',
                4: '沉降速率',
                5: '横向收敛变形',
                6: '渗漏水'
            }
            row.append(mainDisease[minIx])

            methods = {
                1: '日常维护',
                2: '小修',
                3: '中修',
                4: '大修'
            }
            row.append(methods[level])

            minRing = data['comprehensiveValue'].argmin()
            ringNumber = data['ringNumber'].iloc[minRing]
            s = data['comprehensiveValue'].iloc[minRing]
            level = score2Level(s)
            lroman = level2Roman(level)
            row.extend([ringNumber, s, lroman])

            minRingScore = data.iloc[minRing, 8:15]
            minRingScore.index = range(7)
            minIx = minRingScore.argmin()
            row.append(mainDisease[minIx])

            dataTable.append(row)
        except:
            print('open solution csv except')

    print(dataTable)
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
