from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ..usr.user import login_required
from ..db.db import get_db


def getDataByDate(date):
    d = {'编号': list(range(28)), '环号': list(range(28)), '沉降': list(range(28))}
    return d


def solutionRealize():
    # mode：'1'为导入数据, '2'为查看、编辑数据
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == '1':
            date = request.form.get('date')
            return redirect(url_for('project.data', mode=1, date=date))
        else:
            date = request.form.get('date')
            return redirect(url_for('project.data', mode=2, date=date))
    else:
        mode = request.args.get('mode')
        if mode == '1':
            date = request.args.get('date')
            data = getDataByDate(date)
            data = {'heads': ['编号', '环号', '沉降'], 'datas': data}
            dataSum = 28
            return render_template('project/data/dataImport.html', date=date, data=data, dataSum=dataSum)
        else:
            date = request.args.get('date')
            data = getDataByDate(date)
            data = {'heads': ['编号', '环号', '沉降'], 'datas': data}
            dataSum = 18
            return render_template('project/data/dataEdit.html', date=date, data=data, dataSum=dataSum)
