from flask_admin import Admin
from main import app
from flask_admin.contrib.sqla import ModelView
from flask import current_app,redirect,url_for,request
from models.models import db,User,DianYing,Count,XinXi,Collection

class MyModelView(ModelView):
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class MyUser(MyModelView):
    column_labels = dict(
        name='账号',
        email='邮箱',
        pwd='密码'
    )

class MyDianYing(MyModelView):
    column_labels = dict(
        movie = '电影名',
        score = '评分',
        num = '评价人数',
        star5 = '评五星人数',
        star4 = '评四星人数',
        star3 = '评三星人数',
        star2 = '评二星人数',
        star1 = '评一星人数',
        short = '短评数',
        director = '导演',
        writer = '编剧',
        actor1 = '演员 1',
        actor2 = '演员 2',
        actor3 = '演员 3',
        type1 = '类型1',
        type2 = '类型2',
        region = '制片地区',
        year = '上映年份',
        month = '上映月份',
        time = '片长',
        url = '链接'
    )

class MyCount(MyModelView):
    column_labels = dict(
        datetiems='日期',
        piaofang = '票房',
        date = '更新日期'
    )

class MyXinXi(MyModelView):
    column_labels = dict(
        name='电影名',
        piaofang = '票房',
        movieId = '电影id',
        days = '上映天数',
        datetiems = '日期'
    )
    column_searchable_list = ['name']

class MyCollection(MyModelView):
    column_labels = dict(
        case_item_id = '电影',
        user_id = '用户'
    )

admin = Admin(app=app, name='后台管理系统',template_mode='bootstrap3', base_template='admin/mybase.html')
admin.add_view(MyUser(User, db.session,name='用户管理'))
admin.add_view(MyDianYing(DianYing, db.session,name='电影数据管理'))
admin.add_view(MyCollection(Collection, db.session,name='用户收藏管理'))
admin.add_view(MyCount(Count, db.session,name='总票房数据管理'))
admin.add_view(MyXinXi(XinXi, db.session,name='电影票房数据管理'))


if __name__ == '__main__':
    app.run(debug=True)