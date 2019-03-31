import os
import sys

import numpy as np
import pandas as pd
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .evaluation import getSolution, saveSolutionImage


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['csv'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getPath(name):
    return current_app.static_folder + '/data/'+g.user['username']+'/'+name+'/'


def getPathRel(name):
    return '/static/data/'+g.user['username']+'/'+name+'/'


def float2point(data):
    for col in data:
        a = data[col]
        if a.dtype == np.float:
            data[col] = (a*100).apply(int)/100
    return data


def saveProjectDiseaseData(name, date, file):
    if file.filename == '':
        flash('No selected file')
        return False
    if file and allowed_file(file.filename):
        path = getPath(name)+'disease'
        file.save(os.path.join(path, date+'.csv'))

        try:
            fpath = path+'/'+date+'.csv'
            data = pd.read_csv(fpath, engine='python')
            data = float2point(data)
            data.to_csv(fpath, index=False)
        except:
            print('can not open csv file')
        return True
    return False


def generateImage(name, date, data):
    path = getPath(name)+'solution/image/'+date+'/'
    saveSolutionImage(data, path)
    pass


def processData(name, date):
    path = getPath(name)
    fpath = path+'disease/'+date+'.csv'
    file = os.path.normpath(fpath)
    data = pd.read_csv(file, engine='python')

    print(data.shape, file=sys.stdout)
    s = getSolution(data)
    spath = path+'solution/'+date+'.csv'
    s = float2point(s)
    s.to_csv(spath)

    generateImage(name, date, s)


def checkDate(name, date):
    setProjectData.setProjectDateDB(name, date)
    try:
        path = getPath(name)+'solution/image/'+date
        os.makedirs(path)
    except OSError:
        pass


def getAllDiseaseData(name):
    # path = getPath(name)+'disease/'
    rpath = getPathRel(name)+'disease/'
    dataTable = []

    d = getProjectData.getProjectDateDB(name)
    dates = sorted(set(map(lambda x: x['date'], d)))
    for i, date in enumerate(dates):
        # date = dates[i-1]
        row = [i, date]
        try:
            downloadPath = rpath+date+'.csv'
            dateurl = url_for('project.dataDateData', name=name, date=date)
            row.extend([downloadPath, dateurl])
            dataTable.append(row)
        except:
            print('open disease csv except')

    return dataTable


def dataRealize():
    name = request.values.get('name')
    mode = request.values.get('mode')
    date = request.values.get('date')

    datas = {}
    datas['name'] = name
    datas['date'] = date

    # project_id = getProjectData.getProjectIdDB(name)
    if request.method == 'POST':
        if mode == '1':
            file = request.files['dataFile']
            checkDate(name, date)
            if saveProjectDiseaseData(name, date, file):
                processData(name, date)
            return redirect(url_for('project.data', name=name, mode=1, date=date))
        else:
            return redirect(url_for('project.data', name=name, mode=2, date=date))
    else:
        print("GET", file=sys.stdout)
        if mode == '1':
            if date:
                path = getPath(name)+'disease'
                fpath = path+'/'+date+'.csv'
                file = os.path.normpath(fpath)
                data = pd.read_csv(file, engine='python')
                datas['data'] = data
                print('read_csv data', file=sys.stdout)
            return render_template('project/data/dataImport.html', datas=datas)
        else:
            data = getAllDiseaseData(name)
            datas['data'] = data
            return render_template('project/data/dataEdit.html', datas=datas)


def getDataDateData(name, date):
    path = getPath(name)+'disease/'+date+'.csv'
    try:
        data = pd.read_csv(path, engine='python')
    except:
        print('open disease csv except')
    return data


def dataDateDataRealize():
    name = request.values.get('name')
    date = request.values.get('date')
    datas = {}
    datas['name'] = name
    datas['date'] = date
    print(request.values, file=sys.stdout)
    if request.method == 'POST':
        return redirect(url_for('project.dataDateData', name=name, date=date))
    else:
        data = getDataDateData(name, date)
        datas['data'] = data.T
        return render_template('project/data/dataDateData.html', datas=datas)
