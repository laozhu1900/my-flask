# -*- coding: utf-8-*-

from datetime import datetime, time
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from app import db, login_manager
import hashlib

reload(sys)
sys.setdefaultencoding('utf8')


class Permission:
    READ = 0x01
    WRITE = 0x02
    UPDATE = 0x04
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.READ |
                     Permission.WRITE, True),
            'Professor': (Permission.READ |
                          Permission.WRITE |
                          Permission.UPDATE, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    class_info = db.Column(db.String(64))
    name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(permissions=3).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    @staticmethod
    def insert_subject():
        sub = ['数据结构', 'python基础']
        for s in sub:
            subject = Subject(name=s)
            db.session.add(subject)
            db.session.commit()


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.Text())
    options = db.Column(db.Text())
    answer = db.Column(db.String(64))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    kn_point_id = db.Column(db.Integer, db.ForeignKey('knPoints.id'))
    kn_point_counts = db.Column(db.Integer, default=1)
    degree = db.Column(db.String(64))
    question_type_id = db.Column(db.Integer, db.ForeignKey('qTypes.id'))
    appearance = db.Column(db.Integer, default=0)
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    accuracy = db.Column(db.Float, default=0.0)
    question_since = db.Column(db.DateTime(), default=datetime.utcnow)

    @staticmethod
    def insert_questions():
        f = open('/home/zhuzw/git/flasky/sql/data.txt', 'r')
        lines = f.readlines()
        f.close()
        s = Subject.query.filter_by(name='数据结构').first()

        for line in lines:
            tmp = line.replace("\n", "").split("|")
            q = Question()
            q.context = tmp[0]
            q.options = tmp[1]
            q.answer = tmp[2]
            qt = QuestionType.query.filter_by(name=tmp[3]).first()
            q.question_type_id = qt.id
            q.subject_id = s.id

            knp = KnowledgePoint.query.filter_by(name=tmp[4]).first()
            q.kn_point_id = knp.id
            q.degree = tmp[5]
            q.accuracy = 0
            q.appearance = 0
            u = User.query.filter_by(username="prozhu").first()
            q.professor_id = u.id

            db.session.add(q)
            db.session.commit()


class QuestionType(db.Model):
    __tablename__ = 'qTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    score = db.Column(db.Integer)

    @staticmethod
    def insert_types():
        types = {"选择题": 3, "判断题": 2, "填空题": 5}
        for k in types.keys():
            qt = QuestionType(name=k, score=types[k])
            db.session.add(qt)
        db.session.commit()


class KnowledgePoint(db.Model):
    __tablename__ = 'knPoints'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    @staticmethod
    def get_kn_points():
        kn_points = KnowledgePoint.query.all()
        kn_points_list = []
        for kp in kn_points:
            kn_points_list.append((kp.id, kp.name))
        return kn_points_list


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    @staticmethod
    def insert_chapters():
        s = Subject.query.filter_by(name='数据结构').first()
        s2 = Subject.query.filter_by(name='python基础').first()
        structure = {
            "算法分析": ("最大子序列和问题的求解", "时间空间复杂度", "贪婪算法", "分治算法", "动态规划", "随机化算法", "回溯算法"),
            "表、栈和队列": ["单链表", "双向链表", "栈ADT", "队列ADT"],
            "树": ["二叉树", "AVL树", "伸展树", "树的遍历", "B树"],
            "排序": ["插入排序", "希尔排序", "归并排序", "快速排序", "堆排序", "冒泡排序"],
            "优先队列": ["模型", "二叉堆", "d-堆", "左式堆", "斜堆", "二项队列"],
        }

        structure2 = {'模块':['变量赋值','赋值操作符','增量赋值','多重赋值','多元赋值'],
              '标识符':['合法的Python标识符','关键字','内建','专用下划线标识符'],
              '基本风格指南':['模块结构和布局','在主程序中书写测试代码'],
              '内存管理':['变量定义','动态类型','内存分配','引用计数','垃圾收集']

        }
        for chapter in structure.keys():

            ch = Chapter(name=chapter, subject_id=s.id)
            db.session.add(ch)
            db.session.commit()

            c = Chapter.query.filter_by(name=chapter).first()

            for point in structure[chapter]:
                kn = KnowledgePoint(name=point, chapter_id=c.id, subject_id=s.id)
                db.session.add(kn)

        for chapter in structure2.keys():

            ch = Chapter(name=chapter, subject_id=s2.id)
            db.session.add(ch)
            db.session.commit()

            c = Chapter.query.filter_by(name=chapter).first()

            for point in structure2[chapter]:
                kn = KnowledgePoint(name=point, chapter_id=c.id, subject_id=s2.id)
                db.session.add(kn)

        db.session.commit()