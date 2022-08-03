import time
from time import sleep

from flask import jsonify, Blueprint
from flask_login import login_user, login_required, logout_user
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from app.models import User
from app.create_app import db, login_manager
from app.common.check import check_email, check_phone


@login_manager.user_loader
def user_loader(uid):
    return db.session.query(User).filter_by(uid=uid).first()


class Account(Resource):
    def __init__(self):
        # self.logger = current_app.logger
        # self.config = current_app.config
        self.parser = RequestParser()
        self.parser.add_argument('uid', type=str, help='Rate cannot be converted', location=['args'])
        self.parser.add_argument('pwd', type=str, help='Rate cannot be converted', location=['args'])
        self.parser.add_argument('email', type=str, help='Rate cannot be converted', location=['args'])
        self.parser.add_argument('phone', type=str, help='Rate cannot be converted', location=['args'])
        self.request = self.parser.parse_args()

    def get(self):
        uid, pwd = self.request.uid, self.request.pwd
        print(uid, pwd)
        mysql = db.session
        user = mysql.query(User).get(uid)  # <class 'app.models.User'> or None
        if user:
            if user.pwd == pwd:
                login_user(user)
                return jsonify({'status': 1})
            else:
                return jsonify({'status': 0, 'msg': 'account and password not match'})
        else:
            return jsonify({'status': 0, 'msg': 'account not found'})

    @login_required
    def post(self):
        # print(current_user.uid)
        # print(current_user.is_authenticated)
        mysql = db.session
        if mysql.query(User).get(self.request.uid):  # <class 'app.models.User'> or None
            return jsonify({'status': 0, 'msg': 'account exist, choose another account'})
        elif not check_email(self.request.email):
            return jsonify({'status': 0, 'msg': 'email format error'})
        elif not check_phone(self.request.phone):
            return jsonify({'status': 0, 'msg': 'phone format error'})
        else:
            user = User()
            user.uid = self.request.uid
            user.pwd = self.request.pwd
            user.email = self.request.email
            user.phone = self.request.phone
            mysql.add(user)
            mysql.commit()
            return jsonify({'status': 1, 'msg': 'account establish success'})

    @login_required
    def delete(self):
        logout_user()


bp = Blueprint('account', __name__, url_prefix='/api/v1/account')
api = Api(bp)
api.add_resource(Account, '/', endpoint='index')
