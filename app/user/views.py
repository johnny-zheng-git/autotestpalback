######################################
# Time:2020/02/09
# alter: ZWQ
######################################

from flask_restplus import Resource, reqparse
from .models import UserModel, RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, get_raw_jwt
from flask_restplus import Api

from flask import Blueprint
from flask_restplus import Api
# from
from app.log import log

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
user_mold = Blueprint('user_mold', __name__)
api = Api(user_mold, version='1.0', title='USER API',
          description='USER API', authorizations=authorizations, security='apikey')

parser = reqparse.RequestParser()  # 设置接收参数
parser.add_argument('username', type=str, help='username field cannot be blank', required=True)
parser.add_argument('password', type=str, help='password field cannot be blank', required=True)


class Userlogin(Resource):
    @api.doc(params={'username': '用户名', 'password': '密码'})
    def post(self):
        data = parser.parse_args()
        log.log_recv(data["username"],data)
        print("=========>", data)
        user = UserModel.find_by_username(data['username'])
        print('=======', user.id)
        if not user:
            return {
                'message': f'User {data["username"]} don\'t exist1',
                'code': 1
            }
        if UserModel.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity={'username':data["username"],'userid':user.id})
            refresh_token = create_refresh_token(identity={'username':data["username"],'userid':user.id})
            send_data = {
                'msg': f'logged in as {data["username"]}',
                'code': 0,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            log.log_send(data["username"],send_data)
            return send_data
        else:
            send_data = {
                'message': f'User {data["username"]} don\'t exist2',
                'code': 1
            }
            log.log_send(data["username"],send_data)
            return send_data


class UserRegistration(Resource):
    @api.doc(params={'username': '用户名', 'password': '密码'})
    def post(self):
        data = parser.parse_args()
        log.log_recv(data.username,data)
        if UserModel.find_by_username(data['username']):
            return {
                'msg': f'{data["username"]} has been registered',
                'code': 1,
            }
        new_user = UserModel(username=data["username"], password=UserModel.generate_hash(data['password']))
        try:
            new_user.save_to_db()
            log().logger.info(f"用户{data['username']}已注册")
            # access_token = create_access_token(identity=data['username'])
            # refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': f'User {data["username"]} was created',
                # 'access_token': access_token,
                # 'refresh_token': refresh_token,
                'code': 0
            }
        except:
            return {'messaeg': 'Something went wrong', 'code': 1}, 500
