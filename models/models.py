import flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from sqlalchemy import or_, and_
from flask_babelex import Babel
from flask_security import Security, SQLAlchemySessionUserDatastore, \
    UserMixin, RoleMixin, login_required, auth_token_required, http_auth_required

app = flask.Flask(
    __name__,
    template_folder=os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))) +
    os.sep +
    'templates',
    static_folder=os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))) +
    os.sep +
    'static')

babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SECRET_KEY'] = 'kyes'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'douban.db'))
app.config['SECURITY_PASSWORD_SALT'] = '123456789'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'


db = SQLAlchemy(app)

# 创建模型
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return "<{} 用户 {} 权限>".format(self.user_id,self.role_id)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<{} 权限>".format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username  = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('user', lazy='dynamic'))

    def __repr__(self):
        return "<{} 用户>".format(self.username)


class DianYing(db.Model):
    __tablename__ = 'DianYing'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    movie = db.Column(db.String(52),name='电影名')
    score = db.Column(db.Float,name='评分')
    num = db.Column(db.Float,name='评价人数')
    star5 = db.Column(db.Float, name='评五星人数')
    star4 = db.Column(db.Float, name='评四星人数')
    star3 = db.Column(db.Float, name='评三星人数')
    star2 = db.Column(db.Float, name='评二星人数')
    star1 = db.Column(db.Float, name='评一星人数')
    short = db.Column(db.Float, name='短评数')
    director = db.Column(db.String(104), name='导演')
    writer = db.Column(db.String(104), name='编剧')
    actor1 = db.Column(db.String(104), name='演员 1')
    actor2 = db.Column(db.String(104), name='演员 2')
    actor3 = db.Column(db.String(104), name='演员 3')
    type1 = db.Column(db.String(104), name='类型1')
    type2 = db.Column(db.String(104), name='类型2')
    region = db.Column(db.String(104), name='制片地区')
    year = db.Column(db.String(104), name='上映年份')
    month = db.Column(db.String(104), name='上映月份')
    time = db.Column(db.Float, name='片长')
    url = db.Column(db.String(104),name='链接')

    def __repr__(self):
        return "<{}DianYing>".format(self.movie)


class Count(db.Model):
    __tablename__ = 'count'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    datetiems = db.Column(db.String(104),name='日期')
    piaofang = db.Column(db.Float, name='票房')
    date = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    def __str__(self):
        return "<{}电影票房>".format(self.datetiems)




class XinXi(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(104),name='电影名')
    piaofang = db.Column(db.Float, name='票房')
    movieId = db.Column(db.Float, name='电影id')
    days = db.Column(db.String(104),name='上映天数')
    datetiems = db.Column(db.String(104),name='日期')
    date = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    def __str__(self):
        return "<{}电影票房>".format(self.name)


class Collection(db.Model):
    __tablename__ = 'Collection'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    case_item_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    datetime = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    def __repr__(self):
        return "<{} 收藏>".format(self.user_id)


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()

    # # 设置flask-security
    # user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # security = Security(app, user_datastore)
    # user_datastore.create_role(name='admin', description='管理员')  # 注册管理员权限
    # user_datastore.create_role(name='User', description='普通用户')  # 注册用户权限
    # db.session.commit()
    # new_user = user_datastore.create_user(username='admin', password='root123456', email='123@qq.com',
    #                                       active=True)  # 注册管理员
    # normal_role = user_datastore.find_role('admin')
    # db.session.add(new_user)
    # user_datastore.add_role_to_user(new_user, normal_role)
    # db.session.commit()

