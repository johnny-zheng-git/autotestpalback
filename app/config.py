######################################
# Time:2020/03/16
# alter: ZWQ
######################################
class BaseConfig(object):
    SECRET_KEY = 'zhengwenqaing'
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/flaskr"
    # MAX_OVERFLOW = 5,  # max_overflow=5 必须大写
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = False
    TESTING = False
    DB = {
    }
    LOG_DIR = ''
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mysql+pymysql://{self.DB['user']}:{self.DB['pwd']}@{self.DB['host']}:{self.DB['port']}/{self.DB['db']}"

class ProduceConfig(BaseConfig):
    DB = {
        "user": "root",
        "pwd": "cPHWFPtp55WE4Z1q",
        "host": "cdb-ovrbs6o6.cd.tencentcdb.com",
        "port": 10055,
        "db": "test2"
    }
    HOST = "0.0.0.0"
    PORT = 8080
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:cPHWFPtp55WE4Z1q@cdb-ovrbs6o6.cd.tencentcdb.com:10055/test2"

class DevelopmentConfig(BaseConfig):
    DB = {
        "user": "root",
        "pwd": "123456",
        "host": "127.0.0.1",
        "port": 3306,
        "db": "adam"
    }
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 打印sql语句
    LOG_DIR = ''

class TestingConfig(BaseConfig):
    DB = {
        "user": "root",
        "pwd": "123456",
        "host": "127.0.0.1",
        "port": 3306,
        "db": "flaskr"
    }
    TESTING = True
