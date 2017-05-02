# coding=utf-8
import sys
from app import db
from app.models import Question, QuestionType, User


@staticmethod
def insert_questions():
    f = open('/home/zhuzw/git/flasky/sql/data.txt', 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        print line
        tmp = line.replace("\n", "").split("|")
        q = Question()
        q.context = tmp[0]
        q.options = tmp[1]
        q.answer = tmp[2]
        qt = QuestionType.query.filter_by(name=tmp[3]).first()
        q.question_type = qt.id
        q.kn_point = tmp[4]
        q.degree = tmp[5]
        q.accuracy = 0
        q.appearance = 0
        u = User.query.filter_by(username="prozhu").first()
        q.professor_id = u.id

        if q.question_type is "选择题":
            q.score = 3
        elif q.question_type is "判断题":
            q.score = 2
        elif q.question_type is "填空题":
            q.score = 5
        elif q.question_type is "主观题":
            q.score = 10
        else:
            print "error"
            print line
            sys.exit()
        db.session.add(q)
        db.session.commit()



