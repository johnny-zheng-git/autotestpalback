######################################
# Time:2020/03/16
# alter: ZWQ
######################################

from .views import *


api.add_resource(Userlogin, '/login')
api.add_resource(UserRegistration,'/registration')