######################################
# Time:2020/01/30
# alter: ZWQ
######################################

from app.common import db

from passlib.hash import pbkdf2_sha256 as sha256



class UserModel(db.Model):
    __tablename__ = 'users'
    __table_agrs__ = {"extend_eisting": True}  # 如果表已经被创建过,需要加这个参数提供扩展
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False, info="用户名")
    password = db.Column(db.String(120), nullable=False, info="密码")

    def save_to_db(self):
        '''创建实例，调用save_to_db保存数据'''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        '''调用类方法，按username查询用户信息'''
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        '''返回所有的用户'''

        def to_json(x):
            return {'username': x.username, 'password': x.password}

        return {"user": list(map(lambda x: to_json(x), UserModel.query.all()))}  # 直接用to_json

    @classmethod
    def delete_all(cls):
        try:
            num_rows_delete = db.session.query(cls)
            db.session.commit()
            return {'message': f"{num_rows_delete} row(s) deleted"}
        except:
            return {'message': "Someting went wrong"}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
