from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager

class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Employee': (Permission.GENERAL, 'main', True),
            'Administrator': (Permission.ADMINISTER,'admin', False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)
        #if self.role is None:
        #    if self.email == current_app.config['ADMIN_EMAIL']:
        #        self.role = Role.query.filter_by(
        #            permissions=Permission.ADMINISTER).first()
        #    if self.role is None:
        #        self.role = Role.query.filter_by(default=True).first()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee \'%s\'>' % self.full_name()

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))