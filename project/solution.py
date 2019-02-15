import sys
import pandas

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ..usr.user import login_required
from ..db.db import get_db



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
            return render_template('project/solution/solutionData.html', datas=datas)
        elif mode == '3':
            return render_template('project/solution/solutionCurve.html', datas=datas)
        else:
            return render_template('project/solution/solutionReport.html', datas=datas)
