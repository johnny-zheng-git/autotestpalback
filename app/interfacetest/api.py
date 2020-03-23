######################################
# Time:2020/02/09
# alter: ZWQ
######################################

from flask_restplus import Resource, reqparse
from .models import ProjectModel
from app.user.models import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, get_raw_jwt

from flask import Blueprint
from flask_restplus import Api
from app.log import log
from app.common import db
from sqlalchemy import and_

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
project_mold = Blueprint('project_mold', __name__)
api = Api(project_mold, version='1.0', title='USER API',
          description='Project API', authorizations=authorizations, security='apikey')

parser = reqparse.RequestParser()  # 设置接收参数
parser.add_argument('project_name', type=str)
parser.add_argument('project_v', type=str)
parser.add_argument('project_desc', type=str)
parser.add_argument('user_id', type=int)
parser.add_argument('project_state', type=int)
parser.add_argument('project_id', type=int)


class ProjectAdd(Resource):
    @jwt_required
    @api.doc(params={'project_name': '项目名称', 'project_v': '项目版本', 'project_desc': '项目描述'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        log.log_recv(user_id, data)
        print("=========>", data)
        try:
            project_name = data['project_name']
            project_v = data['project_v']
            project_desc = data['project_desc']
            if project_name == "":
                raise ("project_name不能为空")
            if project_v == "":
                raise ("project_v不能为空")
            if project_desc == "":
                raise ("project_desc不能为空")
        except Exception as e:
            send_data = {
                'code': 1,
                'message': "parameter error"
            }
            log.log_send(user_id, send_data)
            return send_data
        try:

            new_project = ProjectModel(project_name=project_name, project_v=project_v, project_desc=project_desc,
                                       user_id=user_id)
            new_project.save_to_db()

            send_data = {
                'message': f'project {project_name} was created',
                'code': 0
            }
            log.log_send(user_id, send_data)
            return send_data
        except:
            send_data = {'messaeg': 'Something went wrong', 'code': 1}
            log.log_send(user_id, send_data)
            return send_data, 500


class Projectselect(Resource):
    @jwt_required
    @api.doc(params={'project_name': '项目名称'})
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()['userid']
        log.log_recv(user_id, data)
        try:
            print(data.project_name)
            all_results = db.session.query(ProjectModel.project_name, ProjectModel.project_desc, ProjectModel.project_v,
                                           ProjectModel.create_time, ProjectModel.project_id, ProjectModel.updata_time,
                                           ProjectModel.project_state, UserModel.username).filter(and_(
                ProjectModel.project_name.like(
                    "%" + data.project_name + "%") if data.project_name is not None else user_id != '',ProjectModel.delete_sign==0)
            ).filter(ProjectModel.user_id == UserModel.id).all() #paginate(page=1, per_page=200,error_out=False)
            # print('===========================',len(all_results.items))
            # pn = User.query.paginate(2, 3)
            project_list = []
            for i in all_results:
                # print(i)
                project_data = {
                    'project_name': i.project_name,
                    'project_id': i.project_id,
                    'project_v': i.project_v,
                    'project_desc': i.project_desc,
                    'user_name': i.username,
                    'create_time': str(i.create_time),
                    'updata_time': str(i.updata_time),
                    'project_state': i.project_state,
                }
                project_list.append(project_data)
            send_data = {
                'code': 0,
                'message': "SUCCESS",
                'project': project_list
            }
            log.log_send(user_id, send_data)
            return send_data
        except Exception as e:
            # print(e)
            send_data = {'messaeg': 'Something went wrong', 'code': 1}
            log.log_send(user_id, send_data)
            return send_data, 500


class ProjectDelete(Resource):
    @jwt_required
    @api.doc(params={"project_id": "项目id"})
    def post(self):
        data = parser.parse_args()
        print("========================",data)
        user_id = get_jwt_identity()['userid']
        log.log_recv(user_id, data)
        try:
            ProjectModel.query.filter_by(project_id=data.project_id).update({'delete_sign':1})
            send_data = {
                'message': 'SUCCESS',
                'code': 0
            }
            log.log_send(user_id, send_data)
            return send_data
        except Exception as e:
            print(e)
            send_data = {
                'message': 'FAIL',
                'code': 1
            }
            log.log_send(user_id, send_data)
            log.log_send(user_id, str(e))
            return send_data, 500
