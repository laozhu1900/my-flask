# -*- coding:utf-8 -*-


from flask import redirect, url_for, render_template, flash, Session
from flask.ext.login import login_required, current_user
import sys
from app import db
from app.decorators import admin_required
from app.main import main
from app.main.forms import EditProfileForm, EditProfileAdminForm, SearchForm, AdminEditUserForm
from ..models import User, Role, Question, QuestionType, Chapter, KnowledgePoint, Subject

reload(sys)
sys.setdefaultencoding('utf8')


@main.route('/', methods=['GET', 'POST'])
def index():
    subject_results = Subject.query.all()
    form = SearchForm()

    if form.validate_on_submit():
        context = form.context.data
        results = Question.query.filter(Question.context.like('%' + context + '%')).all()
        return render_template('search_results.html', results=results, count=len(results))
    return render_template('index.html', form=form,subject_results=subject_results)


@main.route('/structure/<subject>', methods=['GET', 'POST'])
def structure(subject):
    subject_id = Subject.query.filter_by(name=subject).first().id

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    results = {}
    for ch in chapters:
        kns = KnowledgePoint.query.filter_by(chapter_id=ch.id).all()
        results[ch.name] = []
        for kn in kns:
            results[ch.name].append(kn.name)

    return render_template('structure.html', results=results, subject=subject)


@main.route('/<question_type_id>', methods=['GET', 'POST'])
def search(question_type_id):
    qt = QuestionType.query.filter_by(name=question_type_id).first()
    results = Question.query.filter_by(question_type_id=qt.id).all()
    return render_template('search_results.html', results=results, count=len(results))


@main.route('/user/<username>')
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=u)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.class_info = form.class_info.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('信息已被更新.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.class_info.data = current_user.class_info
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.class_info = form.class_info.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('你的信息已经更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.class_info.data = user.class_info
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/organize-user/', methods=['GET', 'POST'])
@login_required
@admin_required
def organize_user():
    role_id = Role.query.filter_by(name='Administrator').first().id
    results = User.query.filter(User.role_id.notlike(role_id)).all()
    return render_template('user_list.html', results=results)


@main.route('/delete-user/<int:uid>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(uid):
    u = User.query.filter_by(id=uid).first()
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('main.organize_user'))


@main.route('/edit-user/<int:uid>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(uid):

    form = AdminEditUserForm()
    u = User.query.filter_by(id=uid).first()
    if form.validate_on_submit():
        u.username = form.username.data

        role_id = Role.query.filter_by(name=form.authority.data).first().id
        u.role_id = role_id

        db.session.add(u)
        db.session.commit()
        return render_template('ques/message.html', message='更新成功')

    form.username.data = u.username
    authority = Role.query.filter_by(id=u.role_id).first().name
    form.authority.data = authority

    return render_template('edit_user.html', form=form)


