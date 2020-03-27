######################################
# Time:2020/02/09
# alter: ZWQ
######################################

from flask_restplus import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, get_raw_jwt
from flask import Blueprint
from flask_restplus import Api
import os

from .models import UserModel, RevokedTokenModel
from app.log import logger



file_name = os.path.basename(__file__)

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

# User_Api = api.namespace(name='user',
#                               description='用户模块')


class Userlogin(Resource):
    @api.doc(params={'username': '用户名', 'password': '密码'})
    def post(self):
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        logger.info(f"{user.id}====={data}")
        if not user:
            send_data = {
                'message': f'User {data["username"]} don\'t exist1',
                'code': 1
            }
            logger.error(f"{send_data}")
            return send_data
        if UserModel.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity={'username': data["username"], 'userid': user.id})
            refresh_token = create_refresh_token(identity={'username': data["username"], 'userid': user.id})
            send_data = {
                'msg': f'logged in as {data["username"]}',
                'code': 0,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            logger.info(f'{send_data}')
            return send_data
        else:
            send_data = {
                'message': f'User {data["username"]} don\'t exist2',
                'code': 1
            }
            logger.info(f'{send_data}')
            return send_data


class UserRegistration(Resource):
    @api.doc(params={'username': '用户名', 'password': '密码'})
    def post(self):
        data = parser.parse_args()
        logger.info(f'{data}')
        if UserModel.find_by_username(data['username']):
            send_data = {
                'msg': f'{data["username"]} has been registered',
                'code': 1,
            }
            logger.info(f'{send_data}')
            return send_data
        new_user = UserModel(username=data["username"], password=UserModel.generate_hash(data['password']))
        try:
            new_user.save_to_db()
            send_data = {
                'message': f'User {data["username"]} was created',
                'code': 0
            }
            logger.info(f"{send_data}")
            return send_data
        except Exception as e:
            logger.error(f"{e}")
            return {'messaeg': 'Something went wrong', 'code': 1}, 500


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def get(self):
        user = get_jwt_identity()
        send_data = {'access_token': create_access_token(identity=user), 'code': 0}
        return send_data
