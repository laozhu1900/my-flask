# -*- coding:utf-8 -*-
import sys

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User

reload(sys)
sys.setdefaultencoding('utf8')


class SearchForm(Form):
    context = StringField("请输入搜索内容", validators=[Required("输入不能为空")])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64), Required("真实姓名不能为空")])
    class_info = StringField('班级信息', validators=[Length(0, 64), Required("班级信息不能为空")])
    about_me = TextAreaField('自我描述', validators=[Length(0, 64), Required("自我描述不能为空")])
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名必须是大小写字母和下划线组成')])
    confirmed = BooleanField('是否验证用户')
    role = SelectField('角色', coerce=int)
    name = StringField('真是姓名', validators=[Length(0, 64)])
    class_info = StringField('班级信息', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class AdminEditUserForm(Form):
    username = StringField('用户名', validators=[Length(0, 64)])
    # authority = StringField('权限', validators=[Length(0, 64)])
    authority = SelectField("权限", choices=[('User', '普通用户'), ('Professor','教师')])
    submit = SubmitField('提交')
