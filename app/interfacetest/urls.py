######################################
# Time:2020/03/16
# alter: ZWQ
######################################

from .api import *


api.add_resource(ProjectAdd, '/add')
api.add_resource(Projectselect,'/select')
api.add_resource(ProjectDelete,'/delete')
api.add_resource(ProjectUpdata,'/updata')
api.add_resource(HostAdd,'/hostadd')
api.add_resource(Hostselect,'/hostselect')
api.add_resource(HostDelete,'/hostdelete')
api.add_resource(HostUpdata,'/hostupdata')