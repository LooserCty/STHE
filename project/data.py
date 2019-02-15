import os
import sys

import pandas as pd
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required
from .evaluation import *


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['csv'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getPath(name):
    return current_app.static_folder + '/data/'+g.user['username']+'/'+name+'/'


def saveProjectDiseaseData(name, date, file):
    if file.filename == '':
        flash('No selected file')
        return
    if file and allowed_file(file.filename):
        print(file.filename, file=sys.stdout)
        filename = secure_filename(file.filename)
        print(filename, file=sys.stdout)
        path = getPath(name)+'disease'
        file.save(os.path.join(path, date+'.'+filename))
        # fpath = path+'/病害数据.'+filename
        # file = os.path.normpath(fpath)
        # data = pd.read_csv(file, engine='python')
        # print(data, file=sys.stdout)
        # n = data.shape[0]
        return


def processData(name, date):
    path = getPath(name)
    fpath = path+'disease/'+date+'.csv'
    file = os.path.normpath(fpath)
    data = pd.read_csv(file, engine='python')
    print(data.shape, file=sys.stdout)
    s=getSolution(data)
    spath=path+'solution/'+date+'.csv'
    s.to_csv(spath)


def checkDate(name, date):
    setProjectData.setProjectDateDB(name, date)


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
            saveProjectDiseaseData(name, date, file)
            processData(name, date)
            return redirect(url_for('project.data', name=name, mode=1, date=date))
        else:
            return redirect(url_for('project.data', name=name, mode=2, date=date))
    else:
        print("GET", file=sys.stdout)
        if mode == '1':
            # datas['date'] = '1998-12-01'
            if date:
                path = getPath(name)+'disease'
                fpath = path+'/'+date+'.csv'
                file = os.path.normpath(fpath)
                data = pd.read_csv(file, engine='python')
                datas['data'] = data
                print('read_csv data', file=sys.stdout)
            return render_template('project/data/dataImport.html', datas=datas)
        else:

            return render_template('project/data/dataEdit.html', datas=datas)
