import os
import logzero
import logging
from app.utils import log_path

logfile = os.path.join(log_path, "flask.log").replace("\\", "/")
log_format = '%(color)s[%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s%(end_color)s: %(message)s'
formatter = logzero.LogFormatter(fmt=log_format)
logzero.setup_default_logger(formatter=formatter, logfile=logfile,maxBytes=2e8, backupCount=1)
logzero.loglevel(logging.DEBUG)

logger = logzero.logger

# logzero.logger.debug("hello")
# logzero.logger.info("info")
# logzero.logger.warning("warning")
# logzero.logger.error("error")
# logger.debug("hello")



# formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# logzero.formatter(formatter)
# logzero.loglevel(logging.DEBUG)
# logger = logzero.logger
#
#
# logger.debug("hello %s", "world")
# logger.info("info")
# logger.warning("warn")
# logger.error("error")
#
# try:
#     raise Exception("this is a demo exception")
# except Exception as e:
#     logger.exception(e)


#
# class log:
#     def __init__(self):
#         self.logfile = os.path.join(log_path, "flask.log").replace("\\", "/")
#         logzero.logfile(self.logfile, maxBytes=2e8, backupCount=1, encoding="utf-8")
#         formatter = logging.Formatter('%(asctime)-15s -%(levelname)s: %(message)s')
#         logzero.formatter(formatter)
#         logzero.loglevel(logging.INFO)
#         # print(self.logfile)
#         self.logger = logzero.logger
#
#     @classmethod
#     def log_recv(cls,userid,recv_data,class_name='',file_name=''):
#         cls().logger.info(f"recv=====>file_name:{file_name},classname:{class_name},userid:{userid},message:{recv_data}")
#
#     @classmethod
#     def log_send(cls, userid,recv_data,class_name='',file_name=''):
#         cls().logger.info(f"send=====>file_name:{file_name},classname:{class_name},userid:{userid},message:{recv_data}")
