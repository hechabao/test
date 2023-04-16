# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import random
import traceback

from flask import Flask, request, render_template,jsonify,abort,session,redirect, url_for
import os
from models import models
from models.models import app
import time
from sqlalchemy import or_,and_
import jieba
from flask_security import Security, SQLAlchemySessionUserDatastore, \
    UserMixin, RoleMixin, login_required, auth_token_required, http_auth_required,current_user

user_datastore = SQLAlchemySessionUserDatastore(models.db.session, models.User, models.Role)
security = Security(app, user_datastore)



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    uuid = current_user.is_anonymous
    if uuid:
        return redirect(url_for('logins'))
    if request.method == 'GET':
        datas1 = models.DianYing.query.all()
        results = []
        for da1 in datas1:
            dicts = {}
            dicts['id'] = da1.id
            dicts['movie'] = da1.movie
            dicts['score'] = da1.score
            dicts['num'] = da1.num
            dicts['short'] = da1.short
            dicts['writer'] = da1.writer
            dicts['region'] = da1.region
            dicts['year'] = da1.year
            dicts['month'] = da1.month
            dat1 = models.XinXi.query.filter(models.XinXi.name == da1.movie).all()
            if dat1:
                num = 0
                for da2 in dat1:
                    num += da2.piaofang
                dicts['piaofang'] = num
            else:
                dicts['piaofang'] = 0
            results.append(dicts)
        return render_template('app/index.html',**locals())



@app.route('/shouchang', methods=['GET', 'POST'])
def shouchang():
    uuid = current_user.is_anonymous
    if uuid:
        return redirect(url_for('logins'))
    if request.method == 'GET':
        id1 = request.args.get('id')
        if not models.Collection.query.filter(and_(models.Collection.user_id==uuid,models.Collection.case_item_id==id1)).all():
            models.db.session.add(
                models.Collection(
                    case_item_id = id1,
                    user_id = uuid
                ))
            models.db.session.commit()
        return redirect('/index')


from collections import OrderedDict
import pandas as pd
from models import models
from sqlalchemy import or_,and_
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy
def yuce1(name):
    try:
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
        examDf.head()

        # exam_x 即为feature
        exam_x = examDf.loc[:, '日期']
        # exam_y 即为label
        exam_y = examDf.loc[:, '票房']

        X_train, X_test, y_train, y_test = train_test_split(
            exam_x, exam_y, train_size=0.8)
        # X_train, X_test, y_train, y_test的shape
        # 为(400, 1) (200, 1) (400, 1) (200, 1)

        # 定义模型
        regr_rf = RandomForestRegressor()
        # 集合模型
        x_train = X_train.values.reshape(-1, 1)
        x_test = X_test.values.reshape(-1, 1)

        regr_rf.fit(x_train, y_train)
        # 利用预测
        y_rf = regr_rf.predict(x_test)

        # 评价
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

        return li2[2:]
    except:
        print(traceback.format_exc())
        return []

def yuce2():
    dates = models.Count.query.all()
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
    examDf.head()

    # exam_x 即为feature
    exam_x = examDf.loc[:, '日期']
    # exam_y 即为label
    exam_y = examDf.loc[:, '票房']

    X_train, X_test, y_train, y_test = train_test_split(
        exam_x, exam_y, train_size=0.8)
    # X_train, X_test, y_train, y_test的shape
    # 为(400, 1) (200, 1) (400, 1) (200, 1)

    # 定义模型
    regr_rf = RandomForestRegressor()
    # 集合模型
    x_train = X_train.values.reshape(-1, 1)
    x_test = X_test.values.reshape(-1, 1)

    regr_rf.fit(x_train, y_train)
    # 利用预测
    y_rf = regr_rf.predict(x_test)

    # 评价
    regr_rf.score(x_test, y_test)

    data1 = datetime.datetime.strptime(str(date_day[-1]), '%Y%m%d')
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
        dicts['piaofang'] = round(abs(y_train_pred[i])+random.randint(-1000,1000),2)
        li2.append(dicts)
    print("yuce2 - " + li2)
    return li2[2:]

@app.route('/yuce', methods=['GET', 'POST'])
def yuce():
    if request.method == 'GET':
        result = list(set([i.name for i in models.XinXi.query.all() if len(models.XinXi.query.filter(models.XinXi.name==i.name).all()) > 8]))

        return render_template('app/yuce.html',**locals())
    elif request.method == 'POST':
        result = list(set([i.name for i in models.XinXi.query.all() if len(models.XinXi.query.filter(models.XinXi.name==i.name).all()) > 8]))
        name = request.form.get('name')
        print(name)
        if name == '总票房':
            datas = yuce2()
        else:
            datas = yuce1(name)
        riqi = [i['riqi'] for i in datas]
        piaofang = [i['piaofang'] for i in datas]

        return render_template('app/yuce.html',**locals())




@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        datas1 = models.DianYing.query.all()
        results = []
        for da1 in datas1:
            dicts = {}
            dicts['id'] = da1.id
            dicts['movie'] = da1.movie
            dicts['score'] = da1.score
            dicts['num'] = da1.num
            dicts['short'] = da1.short
            dicts['writer'] = da1.writer
            dicts['region'] = da1.region
            dicts['year'] = da1.year
            dicts['month'] = da1.month
            dat1 = models.XinXi.query.filter(models.XinXi.name==da1.movie).all()
            if dat1:
                num = 0
                for da2 in dat1:
                     num += da2.piaofang
                dicts['piaofang'] = num
            else:
                dicts['piaofang'] = 0
            results.append(dicts)


        return render_template('table.html',**locals())


@app.route('/charts1', methods=['GET', 'POST'])
def charts1():
    if request.method == 'GET':
        #导演作品数量前20的导演
        datas = models.DianYing.query.all()
        daoyans = [i.director for i in datas]
        daoyan_set = list(set(daoyans))
        daoyan_set.sort()
        daoyan_name = []
        daoyan_count = []
        li1 = []
        for resu in daoyan_set:
            li1.append((resu,daoyans.count(resu)))
        li1.sort(key=lambda xx:xx[1],reverse=True)
        for resu in li1[:20]:
            daoyan_name.append(resu[0])
            daoyan_count.append(resu[1])

        #电影评分前20的导演
        pf_dict = []
        li1 = []
        for resu in daoyan_set:
            da1 = models.DianYing.query.filter(models.DianYing.director==resu).all()
            num = 0
            count = 0
            for da2 in da1:
                num += da2.score
                count += 1
            li1.append((resu,round(num/count,2)))
        li1.sort(key=lambda xx:xx[1],reverse=True)
        for resu in li1[:20]:
            pf_dict.append({"name":resu[0],"value":resu[1]})


        return render_template('app/charts1.html',**locals())




@app.route('/keshihua1', methods=['GET', 'POST'])
def daping():
    if request.method == 'GET':
        datas = models.DianYing.query.all()

        datas1 = models.XinXi.query.all()
        names = list(set([i.name for i in datas1]))
        pingfen_name = []
        pingfen_count = []
        li1 = []
        for resu in names:
            value = models.XinXi.query.filter(models.XinXi.name==resu).all()[0].piaofang
            li1.append((resu, value))
        li1.sort(key=lambda xx: xx[1], reverse=True)
        for resu in li1[:10]:
            pingfen_name.append(resu[0])
            pingfen_count.append(resu[1])

        # 各类型电影
        types = list(set([i.type1 for i in datas]))
        itype_list = []
        itype_list_key = []
        itype_count = []
        for itype in types:
            itype_list.append({"name":itype,"value":len(models.DianYing.query.filter(or_(models.DianYing.type1 == itype,models.DianYing.type2 == itype)).all())})
            itype_list_key.append(itype)

        shangying_list = []
        shangying_count = []
        for i in models.Count.query.all():
            shangying_list.append(i.datetiems)
            shangying_count.append(i.piaofang)

        #评分和时长的关系
        score_time = []
        for resu in datas:
            score_time.append([resu.score,resu.time,resu.movie])

        #各星级评分人数
        star_name = ['五星','四星','三星','二星','一星']
        star_count = [
            sum([i.star5 for i in datas if i.star5]),
            sum([i.star4 for i in datas if i.star4]),
            sum([i.star3 for i in datas if i.star3]),
            sum([i.star2 for i in datas if i.star2]),
            sum([i.star1 for i in datas if i.star1]),
        ]

        # 短评数前十电影
        short_name = []
        short_count = []
        li1 = []
        for resu in datas:
            li1.append((resu.movie, resu.short))
        li1.sort(key=lambda xx: xx[1], reverse=True)
        for resu in li1[:20]:
            short_name.append(resu[0])
            short_count.append(resu[1])

        # 评价人数前十电影
        num_name = []
        num_count = []
        li1 = []
        for resu in datas:
            li1.append((resu.movie, resu.num))
        li1.sort(key=lambda xx: xx[1], reverse=True)
        for resu in li1[:10]:
            num_name.append(resu[0])
            num_count.append(resu[1])

        return render_template('daping/index.html',**locals())



@app.route('/keshihua2', methods=['GET', 'POST'])
def keshihua2():
    if request.method == 'GET':
        return render_template('keshihua2.html',**locals())


from flask_security.utils import login_user, logout_user
@app.route('/logins', methods=['GET', 'POST'])
def logins():
    uuid = current_user.is_anonymous
    if not uuid:
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('account/index.html')
    elif request.method=='POST':
        user = request.form.get('user')
        password = request.form.get('password')
        data = models.User.query.filter(and_(models.User.username==user,models.User.password==password)).first()
        if not data:
            return render_template('account/index.html',error='账号密码错误')
        else:
            login_user(data, remember=True)
            return redirect(url_for('index'))



@app.route('/loginsout', methods=['GET'])
def loginsout():
    if request.method=='GET':
        logout_user()
        return redirect(url_for('logins'))


@app.route('/signups', methods=['GET', 'POST'])
def signups():
    uuid = current_user.is_anonymous
    if not uuid:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('account/register.html')
    elif request.method == 'POST':
        user = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('password')
        if models.User.query.filter(models.User.username == user).all():
            return render_template('account/register.html', error='账号名已被注册')
        elif user == '' or password == '' or email == '':
            return render_template('account/register.html', error='输入不能为空')
        else:
            new_user = user_datastore.create_user(username=user, email=email, password=password)
            normal_role = user_datastore.find_role('User')
            models.db.session.add(new_user)
            user_datastore.add_role_to_user(new_user, normal_role)
            models.db.session.commit()
            login_user(new_user, remember=True)

            return redirect(url_for('index'))


def jiequs(li,num=10):
    """自定义的过滤器,截取字符串"""
    if len(li) < num:
        return li[:num]
    else:
        return li[:num] + '...'

app.add_template_filter(jiequs, "jiequ")









