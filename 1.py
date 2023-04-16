from models import models
from collections import OrderedDict
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy
import datetime


name = '穿靴子的猫2'
dates = models.XinXi.query.filter(models.XinXi.name == name).all()
date_day = list(set([int(i.datetiems) for i in dates]))
date_day.sort()

liuliang = []
for i in date_day:
    record_list = models.Count.query.filter(models.Count.datetiems == i).all()
    num = 0
    for reco in record_list:
        num += reco.piaofang
    liuliang.append(num)

# 数据集
examDict = {
    '日期': date_day,
    '票房': liuliang
}

print(examDict)
examOrderedDict = OrderedDict(examDict)
examDf = pd.DataFrame(examOrderedDict)

print(examDf)
# exam_x 即为feature
exam_x = examDf.loc[:, '日期']
# exam_y 即为label
exam_y = examDf.loc[:, '票房']


X_train, X_test, y_train, y_test = train_test_split(
    exam_x, exam_y, train_size=0.8)
#X_train, X_test, y_train, y_test的shape
#为(400, 1) (200, 1) (400, 1) (200, 1)
print(X_train, X_test, y_train, y_test)

#定义模型
regr_rf = RandomForestRegressor()
# 集合模型
x_train = X_train.values.reshape(-1, 1)
x_test = X_test.values.reshape(-1, 1)


regr_rf.fit(x_train, y_train)
# 利用预测
y_rf = regr_rf.predict(x_test)

#评价
regr_rf.score(x_test, y_test)

data1 = datetime.datetime.strptime(str(date_day[-3]), '%Y%m%d')
li1 = []
for i in range(10):
    data1 = data1 + datetime.timedelta(1)
    li1.append([int(data1.strftime('%Y%m%d'))])

li2 = numpy.array(li1)

y_train_pred = regr_rf.predict(li2)

li2 = []
for i in range(len(li1)):
    dicts = {}
    dicts['riqi'] = li1[i][0]
    dicts['piaofang'] = abs(y_train_pred[i])
    li2.append(dicts)
print(li2)


