import os
import sys

import pandas as pd
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from ..db.db import get_db
from ..usr.user import login_required
from .data import getPath


def level2Roman(x):
    tran = {
        1: 'Ⅰ',
        2: 'Ⅱ',
        3: 'Ⅲ',
        4: 'Ⅳ'
    }
    if x in tran:
        return tran[x]
    else:
        return x


def getSolution(name, date):
    # date='2019-02-15'
    path = getPath(name)
    spath = path+'solution/'+date+'.csv'
    file = os.path.normpath(spath)
    data = pd.read_csv(file, engine='python', index_col=0, encoding='utf8')
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
            data = None
            if date:
                df = getSolution(name, date)
                _, m = df.shape
                k = int(ringNumber)
                data = []
                for i in range(m):
                    data.append(df.loc[k][i])
                for i in range(7):
                    data[i] = level2Roman(data[i])
                data[-1] = level2Roman(data[-1])
                data[7:14] = []
                # data=pd.Series(data)
                # data = data.loc[int(ringNumber)]
            if data is not None:
                datas['data'] = data
                datas['success'] = True
            return render_template('project/analysis/analysisCompute.html', datas=datas)
            # return redirect(url_for('project.analysis', name=name, mode=1, date=date, ringNumber=ringNumber))
        else:
            return redirect(url_for('project.analysis', name=name, mode=2))
    else:
        if mode == '1':
            return render_template('project/analysis/analysisCompute.html', datas=datas)
        else:
            return render_template('project/analysis/analysisBasis.html', datas=datas)
