from app import db
from app.models import User, Role, Subject, Question

db.create_all()
Role.insert_roles()

subject = Subject(name='dataStructure')
question = Question(context='单链表是一种随机存储结构', answer='1', degree='1', question_type='choice', appeareace=0,
                    point=1)
User.role = Role.query.filter_by(default=1).first()
pro = User(email='1206953863@qq.com', username='pro', password_hash='pro')
pro.role = Role.query.filter_by(permission=0x04).first()

