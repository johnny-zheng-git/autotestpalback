import os
import logzero
import logging
from app.utils import log_path

# print(os.path.join(log_path, "/log/flask.log").replace("\\", "/"))

class log:
    def __init__(self):
        self.logfile = os.path.join(log_path, "flask.log").replace("\\", "/")
        logzero.logfile(self.logfile, maxBytes=2e8, backupCount=1, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)-15s - [%(filename)s: %(lineno)s] -%(levelname)s: %(message)s')
        logzero.formatter(formatter)
        logzero.loglevel(logging.INFO)
        print(self.logfile)
        self.logger = logzero.logger

    @classmethod
    def log_recv(cls,userid,recv_data):
        cls().logger.info(f"recv=====>userid:{userid},message:{recv_data}")

    @classmethod
    def log_send(cls, userid,save_data):
        cls().logger.info(f"send=====>userid:{userid},message:{save_data}")
