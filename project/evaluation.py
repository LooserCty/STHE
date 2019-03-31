import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

####
# 隶属函数系数由分值标准确定
####

# 隶属函数


def subjectFun(k, alpha, is_reverse):
    def f(x):
        beta = [2, 2, 2, -2]
        a = [k[0]*0.8, (k[0]+k[1])/2, (k[1]+k[2])/2, (k[1]+k[2]*3)/4]

        def u1(x):
            if x <= a[0]:
                return 1
            else:
                return 1/(1+alpha[0]*(x-a[0])**beta[0])

        def u2(x):
            return 1/(1+alpha[1]*(x-a[1])**beta[1])

        def u3(x):
            return 1/(1+alpha[2]*(x-a[2])**beta[2])

        def u4(x):
            if x <= a[3]:
                return 0
            else:
                return 1/(1+alpha[3]*(x-a[3])**beta[3])
        u = [u1, u2, u3, u4]
        subjection = []
        for i in range(4):
            subjection.append(u[i](x))

        level = 1
        if x >= k[2]:
            level = 4
        elif x >= k[1]:
            level = 3
        elif x >= k[0]:
            level = 2

        if is_reverse:
            level = 5-level
            subjection = subjection[::-1]

        subjection = np.array(subjection)
        subjection = subjection/subjection.sum()

        return level, subjection
    return f

# 不同指标的隶属函数集合


def getSubjectFunDict():
    kdict = {
        'crackLength': [3, 5, 10],
        'crackWidth': [1, 3, 5],
        'radiusOfCurvature': [1, 4.7, 15],
        'segmentDislocation': [4, 8, 13],
        'settlementRate': [5, 10, 15],
        'convergenceDeformation': [7.7, 9.6, 13.9]
    }
    alphadict = {
        'crackLength': [2.77777778, 1, 0.16, 1.5625],
        'crackWidth': [25., 1., 1., 0.25],
        'radiusOfCurvature': [25., 0.29218408, 0.03770384, 6.630625],
        'segmentDislocation': [1.5625, 0.25, 0.16, 1.5625],
        'settlementRate': [1., 0.16, 0.16, 1.5625],
        'convergenceDeformation': [0.42165627, 1.10803324, 0.21633315, 1.155625]
    }
    reversedict = {
        'crackLength': 0,
        'crackWidth': 0,
        'radiusOfCurvature': 1,
        'segmentDislocation': 0,
        'settlementRate': 0,
        'convergenceDeformation': 0
    }

    fdict = {}
    for index in kdict:
        fdict[index] = subjectFun(
            kdict[index], alphadict[index], reversedict[index])
    # leakageRate

    def leakageRateFun(x):
        subjection = {
            '湿渍': [0.875, 0.125, 0, 0],
            '滴水': [0.125, 0.75, 0.125, 0],
            '流水': [0, 0.125, 0.75, 0.125],
            '喷水': [0, 0, 0.125, 0.875]
        }
        level = {
            '湿渍': 1,
            '滴水': 2,
            '流水': 3,
            '喷水': 4
        }
        return level[x], subjection[x]
    fdict['leakageRate'] = leakageRateFun

    return fdict

# 合成综合隶属度


def getSubjectionSumm(w):
    def f(s):
        wdict = {
            'crackLength': w[0],
            'crackWidth': w[1],
            'radiusOfCurvature': w[2],
            'segmentDislocation': w[3],
            'settlementRate': w[4],
            'convergenceDeformation': w[5],
            'leakageRate': w[6]
        }
        res = pd.Series([0]*len(s.iloc[0]))
        for ix in s.index:
            res += pd.Series(s[ix])*wdict[ix]
        # print(res.sum())
        return res
    return f

# 计算健康状态评分


def getSubjectionNorm(df):
    w = np.array([0.125, 0.375, 0.625, 0.875][::-1])*100
    norm = df.apply(lambda x: np.sum(np.array(x)*w), axis=1)

    def f(x):
        l = 4
        if x > 75:
            l = 1
        elif x > 50:
            l = 2
        elif x > 25:
            l = 3
        return l
    level = norm.apply(f)
    res = pd.concat([norm, level], axis=1)
    res.columns = ['comprehensiveValue', 'comprehensiveLevel']
    return res

#隶属向量转化为评分
def getSubjectionToScore(s):
    def toScore(subjection):
        w = np.array([0.125, 0.375, 0.625, 0.875][::-1])*100
        subjection=np.array(subjection)
        return (w*subjection).sum()
    
    return s.apply(toScore)


# 获取总的计算结果


def getSolution(data):
    w = [0.14502761, 0.19376159, 0.07834023,
         0.08007087, 0.06553351, 0.0741867, 0.36307949]
    fdict = getSubjectFunDict()
    d = data.iloc[:, 1:]
    level = pd.DataFrame()
    subjection = pd.DataFrame()
    for col in d:
        evaluation = d[col].map(fdict[col])
        level[col] = evaluation.map(lambda x: x[0])
        subjection[col] = evaluation.map(lambda x: x[1])

    # for x in subjection:
    #     for y in subjection[x]:
    #         print(y)
    score = subjection.apply(getSubjectionToScore, axis=0)
    print(score)
    subjectionSumm = subjection.apply(getSubjectionSumm(w), axis=1)
    subjectionSumm.columns = ['subjection1',
                              'subjection2', 'subjection3', 'subjection4']
    subjectionNorm = getSubjectionNorm(subjectionSumm)
    s = pd.concat([level, subjectionSumm, subjectionNorm], axis=1)
    s.index = data.iloc[:, 0]
    return s

# 生成并保存某指标评价结果图像


def saveOneImage(data, path):
    color = {1: 'green', 2: 'yellow', 3: 'orange', 4: 'red'}

    fig = plt.figure(figsize=(20, 2))

    data = data.apply(int)
    n = data.shape[0]
    x = np.linspace(0, n, n+1)
    for i in range(n):
        plt.axvspan(x[i], x[i+1], edgecolor='b',
                    facecolor=color[data.iloc[i]], alpha=1, lw=1)

    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    plt.yticks([])
    plt.tick_params(labelsize=20)
    plt.tight_layout()

    fpath = path+data.name+'.png'
    fig.savefig(fpath, dpi=360)

    plt.close(fig)

# 生成并保存评价结果图像与曲线


def saveSolutionImage(data, path):
    index = ['crackLength', 'crackWidth', 'radiusOfCurvature',	'segmentDislocation',
             'settlementRate',	'convergenceDeformation', 'leakageRate', 'comprehensiveLevel']
    for i in index:
        saveOneImage(data[i], path)
