import sys

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.exceptions import abort

from ..db import getProjectData, setProjectData
from ..db.db import get_db
from ..usr.user import login_required


def getDataByDate(date):
    d = {'编号': list(range(28)), '环号': list(range(28)), '沉降': list(range(28))}
    return d


def dataRealize():
    name = request.values.get('name')
    mode = request.values.get('mode')
    date = request.values.get('date')
    print(request.files,file=sys.stdout)
    file=request.files.get('dataFile',None)
    if file:
        print(type(file.filename),file=sys.stdout)
    if request.method == 'POST':
        if mode == '1':
            return redirect(url_for('project.data', mode=1, date=date))
        else:
            return redirect(url_for('project.data', mode=2, date=date))
    else:
        if mode == '1':
            data = getDataByDate(date)
            data = {'heads': ['编号', '环号', '沉降'], 'datas': data}
            dataSum = 28
            return render_template('project/data/dataImport.html', date=date, data=data, dataSum=dataSum)
        else:
            data = getDataByDate(date)
            data = {'heads': ['编号', '环号', '沉降'], 'datas': data}
            dataSum = 18
            return render_template('project/data/dataEdit.html', date=date, data=data, dataSum=dataSum)
