######################################
# Time:2020/03/16
# alter: ZWQ
######################################

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app import config

# from flask_restplus import Api

# swagger test接口 header 中添加Authorization鉴权，Bearer加空格加access_token
# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'Authorization'
#     }
# }
app = Flask(__name__)
# api = Api(app,authorizations =authorizations,security='apikey')  # swagger security='apikey'使每个请求都要添加token
app.config.from_object(config.DevelopmentConfig())
db = SQLAlchemy()


def create_app():
    @app.before_first_request
    def create_tables():
        '''创建数据库'''
        db.create_all()

    @app.after_request
    def after_request(response):
        """请求自带tocken"""
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    from flask_jwt_extended import JWTManager

    jwt = JWTManager(app)
    from app.user.models import RevokedTokenModel

    @jwt.token_in_blacklist_loader
    def chexk_if_token_in_blacklist(decrpted_token):
        jti = decrpted_token
        return RevokedTokenModel.is_jti_blacklisted(jti)

    db.init_app(app)
    return app
