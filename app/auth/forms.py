# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
import sys
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from app.models import User

reload(sys)
sys.setdefaultencoding('utf8')


class LoginForm(Form):
    email = StringField('邮箱', validators=[Required("邮箱不能为空"), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required("密码不能为空")])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required("邮箱不能为空"), Length(1, 64), Email()])
    username = StringField('用户名', validators=[Required("用户名不能为空"), Length(1, 64)])

    password = PasswordField('密码', validators=[Required("密码不能为空"), EqualTo('password2', message='两次 '
                                                                                              '密码不一样')])

    password2 = PasswordField('密码确认', validators=[Required("确认密码不能为空")])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用.')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')
