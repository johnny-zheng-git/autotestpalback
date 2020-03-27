######################################
# Time:2020/02/09
# alter: ZWQ
######################################

from flask_restplus import Resource, reqparse
from app.user.models import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, get_raw_jwt
from flask import Blueprint
from flask_restplus import Api
from sqlalchemy import and_

from .models import ProjectModel, HostModel, AuthModel
from app.common import db
from app.auth import dataauth
from app.log import logger

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
project_mold = Blueprint('project_mold', __name__)
api = Api(project_mold, version='1.0', title='USER API',
          description='Project API', authorizations=authorizations, security='apikey', name='project_space',
          )
Project_Api = api.namespace(name='project_space',
                            description='项目模块')
Host_Api = api.namespace(name='Host_space',
                         description='项目模块')

parser = reqparse.RequestParser()  # 设置接收参数
parser.add_argument('project_name', type=str)
parser.add_argument('project_v', type=str)
parser.add_argument('project_desc', type=str)
parser.add_argument('user_id', type=int)
parser.add_argument('project_state', type=int)
parser.add_argument('project_id', type=int)
parser.add_argument('host_name', type=str)
parser.add_argument('host_addr', type=str)
parser.add_argument('host_desc', type=str)
parser.add_argument('host_id', type=int)


class ProjectAdd(Resource):
    @jwt_required
    @api.doc(params={'project_name': '项目名称', 'project_v': '项目版本', 'project_desc': '项目描述'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        logger.info(f'{get_jwt_identity()}==={data}')
        project_name = data['project_name']
        project_v = data['project_v']
        project_desc = data['project_desc']
        try:
            new_project = ProjectModel(project_name=project_name, project_v=project_v, project_desc=project_desc,
                                       user_id=user_id)
            new_project.save_to_db()
            #  获取刚刚添加的项目id 存储值auth表
            add_project_auth = AuthModel(project_id=new_project.project_id, user_id=user_id)
            add_project_auth.save_to_db()
            send_data = {
                'message': 'SUCCESS',
                'code': 0
            }
            logger.info(f'{send_data}')
            return send_data
        except Exception as e:
            logger.error(f'{e}')
            send_data = {'messaeg': 'Something went wrong', 'code': 1}
            return send_data, 500


class Projectselect(Resource):
    @jwt_required
    @api.doc(params={'project_name': '项目名称'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        logger.info(f'{get_jwt_identity()}=={data}')
        try:
            #  多表联合查询ProjectModel与UserModel表，获取username及项目信息，通过创建时间倒序
            all_results = db.session.query(ProjectModel.project_name, ProjectModel.project_desc, ProjectModel.project_v,
                                           ProjectModel.create_time, ProjectModel.project_id, ProjectModel.updata_time,
                                           ProjectModel.project_state, UserModel.username).filter(and_(
                ProjectModel.project_name.like(
                    "%" + data.project_name + "%") if data.project_name is not None else user_id != '',
                ProjectModel.delete_sign == 0)
            ).filter(ProjectModel.user_id == UserModel.id).order_by(
                ProjectModel.create_time.desc()).all()
            project_list = []
            for i in all_results:
                if i.project_state == 0:
                    project_state = '进行中'
                elif i.project_state == 1:
                    project_state = '项目暂停'
                else:
                    project_state = '项目结束'
                project_data = {
                    'project_name': i.project_name,
                    'project_id': i.project_id,
                    'project_v': i.project_v,
                    'project_desc': i.project_desc,
                    'user_name': i.username,
                    'create_time': str(i.create_time),
                    'updata_time': str(i.updata_time),
                    'project_state': project_state,
                }
                project_list.append(project_data)
            send_data = {
                'code': 0,
                'message': "SUCCESS",
                'project': project_list
            }
            logger.info(f'{send_data}')
            return send_data
        except Exception as e:
            logger.error(f'{e}')
            send_data = {'messaeg': 'Something went wrong', 'code': 1}
            return send_data, 500


class ProjectDelete(Resource):
    @jwt_required
    @api.doc(params={"project_id": "项目id"})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        logger.info(f'{get_jwt_identity()}=={data}')
        @dataauth(user_id, data.project_id)  # 用户是否有该项目权限
        def fuction():
            try:
                ProjectModel.query.filter_by(project_id=data.project_id).update({'delete_sign': 1})
                send_data = {
                    'message': 'SUCCESS',
                    'code': 0
                }
                logger.info(f'{send_data}')
                return send_data
            except Exception as e:
                logger.error({f'e'})
                send_data = {
                    'message': 'Something went wrong',
                    'code': 1
                }
                return send_data, 500

        return fuction()


class ProjectUpdata(Resource):
    @jwt_required
    @api.doc(params={'project_id': '项目id', 'project_name': '项目名称', 'project_v': '项目版本', 'project_desc': '项目描述',
                     'project_state': '项目状态'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        logger.info(f'{get_jwt_identity()}=={data}')
        @dataauth(user_id, data.project_id)
        def function():
            try:
                ProjectModel.query.filter_by(project_id=data.project_id).update(
                    {'project_name': data.project_name, 'project_v': data.project_v, 'project_desc': data.project_desc,
                     'project_state': data.project_state})
                send_data = {
                    'message': 'SUCCESS',
                    'code': 0
                }
                logger.info(f'{send_data}')
                return send_data
            except Exception as e:
                logger.error(f"{e}")
                send_data = {
                    'message': 'FALSE',
                    'code': 1
                }
                return send_data, 500

        return function()


class Hostselect(Resource):
    @jwt_required
    @api.doc(params={'project_id': '所属项目'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        logger.info(f'{get_jwt_identity()}=={data}')
        try:
            all_results = HostModel.query.filter_by(
                project_id=data.project_id, delete_sign=0).all()
            host_list = []
            for i in all_results:
                host_data = {
                    'host_name': i.host_name,
                    'host_addr': i.host_addr,
                    'host_desc': i.host_desc,
                    'host_id': i.host_id
                }
                host_list.append(host_data)
            send_data = {
                'code': 0,
                'message': "SUCCESS",
                'host_list': host_list
            }
            logger.info(f'{send_data}')
            return send_data
        except Exception as e:
            logger.error(f'{e}')
            send_data = {'messaeg': 'Something went wrong', 'code': 1}
            return send_data, 500


class HostAdd(Resource):
    @jwt_required
    @api.doc(params={'host_name': '名称', 'host_addr': '域名', 'host_desc': '描述', 'project_id': '所属项目id'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        logger.info(f'{get_jwt_identity()}=={data}')
        @dataauth(user_id, data.project_id)
        def function():
            try:
                new_host = HostModel(host_name=data.host_name, host_addr=data.host_addr, host_desc=data.host_desc,
                                     user_id=user_id, project_id=data.project_id)
                new_host.save_to_db()
                send_data = {
                    'message': 'SUCCESS',
                    'code': 0
                }
                logger.info(f'{send_data}')
                return send_data
            except Exception as e:
                logger.error(f'{e}')
                send_data = {'messaeg': 'Something went wrong', 'code': 1}
                return send_data, 500

        return function()


class HostDelete(Resource):
    @jwt_required
    @api.doc(params={'host_id': '主机id'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        todeletehost = HostModel.query.filter_by(host_id=data.host_id)
        logger.info(f'{get_jwt_identity()}=={data}')
        @dataauth(user_id, todeletehost.first().project_id)
        def function():
            try:
                todeletehost.update({'delete_sign': 1})
                send_data = {
                    'message': 'SUCCESS',
                    'code': 0
                }
                logger.info(f'{send_data}')
                return send_data
            except Exception as e:
                logger.error(f'{e}')
                print('=============================', e)
                send_data = {'messaeg': 'Something went wrong', 'code': 1}
                return send_data, 500

        return function()


class HostUpdata(Resource):
    @jwt_required
    @api.doc(params={'host_name': '名称', 'host_addr': '域名', 'host_desc': '描述', 'host_id': '主机id'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        toupdatahost = HostModel.query.filter_by(host_id=data.host_id)
        logger.info(f'{get_jwt_identity()}=={data}')
        @dataauth(user_id, toupdatahost.first().project_id)
        def function():
            try:
                toupdatahost.update(dict(host_name=data.host_name, host_addr=data.host_addr, host_desc=data.host_desc,
                                         user_id=user_id))
                send_data = {
                    'message': 'SUCCESS',
                    'code': 0
                }
                logger.info(f'{send_data}')
                return send_data
            except Exception as e:
                logger.error(f'{e}')
                send_data = {'messaeg': 'Something went wrong', 'code': 1}
                return send_data, 500

        return function()
