######################################
# Time:2020/03/18
# alter: ZWQ
######################################

from app.common import db
import datetime


# from passlib.hash import pbkdf2_sha256 as sha256

# 10.1.1.1 adam_project
class ProjectModel(db.Model):
    __tablename__ = 'adam_project'
    __table_agrs__ = {"extend_eisting": True}  # 如果表已经被创建过,需要加这个参数提供扩展
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True, info='项目id')
    project_name = db.Column(db.String(120), nullable=False, info="项目名称")
    project_v = db.Column(db.String(30), nullable=False, info="项目版本")
    project_desc = db.Column(db.String(500), nullable=False, info="项目描述")
    user_id = db.Column(db.Integer, nullable=False, info="所属用户")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False, info="项目创建时间")
    updata_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False,
                            info="项目更新时间")
    project_state = db.Column(db.Integer, nullable=False, default=0,info="项目状态0进行中1项目暂停2项目结束")
    delete_sign = db.Column(db.Integer, nullable=False, default=0,info="项目删除标志")

    def save_to_db(self):
        '''创建实例，调用save_to_db保存数据'''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_project_name(cls, project_name):
        '''调用类方法，按username查询用户信息'''
        return cls.query.filter(
            cls.project_name.like("%" + project_name + "%") if project_name is not None else ""
        ).all

    # @classmethod
    # def return_all(cls):
    #     '''返回所有的用户'''
    #
    #     def to_json(x):
    #         return {'username': x.username, 'password': x.password}
    #
    #     return {"user": list(map(lambda x: to_json(x), UserModel.query.all()))}  # 直接用to_json

    # @classmethod
    # def delete_all(cls):
    #     try:
    #         num_rows_delete = db.session.query(cls)
    #         db.session.commit()
    #         return {'message': f"{num_rows_delete} row(s) deleted"}
    #     except:
    #         return {'message': "Someting went wrong"}

    # @staticmethod
    # def generate_hash(password):
    #     return sha256.hash(password)
    #
    # @staticmethod
    # def verify_hash(password, hash):
    #     return sha256.verify(password, hash)


# class RevokedTokenModel(db.Model):
#     __tablename__ = 'revoked_tokens'
#     __table_args__ = {"extend_existing": True}
#     id = db.Column(db.Integer, primary_key=True)
#     jti = db.Column(db.String(120))
#
#     def add(self):
#         db.session.add(self)
#         db.session.commit()
#
#     @classmethod
#     def is_jti_blacklisted(cls, jti):
#         query = cls.query.filter_by(jti=jti).first()
#         return bool(query)
