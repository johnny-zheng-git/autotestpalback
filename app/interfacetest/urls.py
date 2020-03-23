######################################
# Time:2020/03/16
# alter: ZWQ
######################################

from .api import *


api.add_resource(ProjectAdd, '/add')
api.add_resource(Projectselect,'/select')
api.add_resource(ProjectDelete,'/delete')
# api.add_resource(UserRegistration,'/registration')