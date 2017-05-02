# -*- coding:utf-8 -*-

from flask.ext.wtf import Form
import sys
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, RadioField
from wtforms.validators import Required, Regexp

reload(sys)
sys.setdefaultencoding('utf8')


class AddQuestionForm(Form):
    context = TextAreaField(validators=[Required()])
    q_type = StringField(validators=[Required()])
    options = TextAreaField(validators=[Required()], default="")
    answer = TextAreaField(validators=[Required()])

    kn_point_id = StringField(validators=[Required()])
    # kn_point_id_2 = SelectField(choices=get_kn_points())
    # kn_point_id_3 = SelectField(choices=get_kn_points())
    # kn_point_id_4 = SelectField(choices=get_kn_points())
    degree = IntegerField(default=1)
    professor_id = StringField(validators=[Required()])
    submit = SubmitField("提交")


class OrganizeQuestionForm(Form):
    choice_num = StringField("请输入选择题数量：", validators=[Required('数量不能为空'),
                                                      Regexp('^[1-9]*$', 0, '输入必须是大于1的整数')])
    judgement_num = StringField("请输入判断题数量：", validators=[Required('数量不能为空'),
                                                         Regexp('^[1-9]*$', 0, '输入必须是大于1的整数')])
    blank_num = StringField("请输入填空题数量：", validators=[Required('数量不能为空'),
                                                     Regexp('^[1-9]*$', 0, '输入必须是大于1的整数')])
    submit = SubmitField("提交")


class EditQuestionForm(Form):
    context = TextAreaField(validators=[Required('不能为空')])
    options = TextAreaField(validators=[Required('不能为空')])
    answer = TextAreaField(validators=[Required('不能为空')])
    kn_point = StringField(validators=[Required('不能为空')])
    submit = SubmitField('提交')


class AnswerForm(Form):
    choiceAnswer = RadioField('选项', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                              validators=[Required('答案不能为空')])
    submit = SubmitField("提交")


class SubjectForm(Form):
    name = StringField('请输入题库名称', validators=[Required('不能为空')])
    subject = SubmitField("提交")


class ChapterForm(Form):
    name = StringField("请输入章节名称", validators=[Required('不能为空')])
    submit = SubmitField("提交")


class KnpointForm(Form):
    name = StringField("请输入章节名称")
    submit = SubmitField("提交")
