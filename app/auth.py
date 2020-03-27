from app.interfacetest.models import AuthModel
from functools import wraps
from app.log import logger

false_json = {
    "code": 1,
    "message": '无权限操作'
}

error_json = {
    "code": 2,
    "message": '服务器错误'
}


#  数据权限验证模块，通过userid 与 projectid 在auth表中查询是否有该项目操作权限
#  视图函数包装，引入auth装饰器
def dataauth(user_id, project_id):
    def auth_decorator(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            try:

                if len(
                        AuthModel.query.filter_by(user_id=user_id,
                                                  project_id=project_id).all()) != 0:
                    return function(*args, **kwargs)
                else:
                    logger.info(f'{false_json}')
                    return false_json
            except Exception as e:
                logger.error(f'{e}')
                print(e)
                return error_json, 500

        return decorator

    return auth_decorator
