import os
import sys

import pandas as pd
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from ..db.db import get_db
from ..usr.user import login_required
from .data import getPath


def getSolution(name, date):
    # date='2019-02-15'
    path = getPath(name)
    spath = path+'solution/'+date+'.csv'
    file = os.path.normpath(spath)
    data = pd.read_csv(file, engine='python', index_col=0)
    # print(data.index, data.columns, file=sys.stdout)
    return data


def analysisRealize():
    # mode：'1'为评价计算, '2'为评价依据
    name = request.values.get('name')
    mode = request.values.get('mode')

    date = request.values.get('date')
    ringNumber = request.values.get('ringNumber')

    datas = {}
    datas['name'] = name
    datas['date'] = date
    datas['ringNumber'] = ringNumber

    if request.method == 'POST':
        if mode == '1':
            # date = request.form.get('date')
            # ringNumber = request.values.get('ringNumber')
            return redirect(url_for('project.analysis', name=name, mode=1, date=date, ringNumber=ringNumber))
        else:
            return redirect(url_for('project.analysis', name=name, mode=2))
    else:
        if mode == '1':
            # date = request.values.get('date')
            # ringNumber = request.values.get('ringNumber')
            # datas['date'] = date
            # datas['ringNumber'] = ringNumber
            data = None
            if date:
                data = getSolution(name, date)
                # print(data.index,type(ringNumber), file=sys.stdout)
                data = data.loc[int(ringNumber)]
            # data=getData(name,date,ringNumber)
            # data = pd.read_csv(
            #     'C:/Users/CTY/Documents/Python/solution.csv', engine='python')
            # data = data.iloc[0, 1:]
            if data is not None:
                datas['data'] = data
                datas['success'] = True
            return render_template('project/analysis/analysisCompute.html', datas=datas)
        else:
            return render_template('project/analysis/analysisBasis.html', datas=datas)
