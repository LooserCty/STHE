import pandas as pd
import numpy as np


####
# 隶属函数系数由分值标准确定
####

# 隶属函数
def subjectFun(k, alpha):
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

        return level, subjection
    return f

# 不同指标的隶属函数集合


def getSubjectFunDict():
    kdict = {
        'crackLength': [2, 5, 10],
        'crackWidth': [1, 3, 5],
        'radiusOfCurvature': [1, 4.7, 15],
        'segmentDislocation': [4, 8, 13],
        'settlementRate': [1, 3, 10],
        'convergenceDeformation': [7, 10, 16]
    }
    alphadict = {
        'crackLength': [6.25, 0.44444444, 0.16, 1.5625],
        'crackWidth': [25., 1., 1., 0.25],
        'radiusOfCurvature': [25., 0.29218408, 0.03770384, 6.630625],
        'segmentDislocation': [1.5625, 0.25, 0.16, 1.5625],
        'settlementRate': [25., 1., 0.08163265, 3.0625],
        'convergenceDeformation': [0.51020408, 0.44444444, 0.11111111, 2.25]
    }
    fdict = {}
    for index in kdict:
        fdict[index] = subjectFun(kdict[index], alphadict[index])
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
        return res
    return f

# 计算健康状态评分


def getSubjectionNorm(df):
    w = np.array([0.125, 0.375, 0.625, 0.875])*100
    norm = df.apply(lambda x: np.sum(np.array(x)*w), axis=1)

    def f(x):
        l = 1
        if x >= 75:
            l = 4
        elif x >= 50:
            l = 3
        elif x >= 25:
            l = 2
        return l
    level = norm.apply(f)
    res = pd.concat([norm, level], axis=1)
    res.columns = ['comprehensiveValue', 'comprehensiveLevel']
    return res

# 获取总的计算结果


def getSolution(data):
    w = [1/7]*7
    fdict = getSubjectFunDict()
    d = data.iloc[:, 1:]
    level = pd.DataFrame()
    subjection = pd.DataFrame()
    for col in d:
        evaluation = d[col].map(fdict[col])
        level[col] = evaluation.map(lambda x: x[0])
        subjection[col] = evaluation.map(lambda x: x[1])
    subjectionSumm = subjection.apply(getSubjectionSumm(w), axis=1)
    subjectionSumm.columns = ['subjection1',
                              'subjection2', 'subjection3', 'subjection4']
    subjectionNorm = getSubjectionNorm(subjectionSumm)
    s = pd.concat([level, subjectionSumm, subjectionNorm], axis=1)
    s.index = data.iloc[:, 0]
    return s
