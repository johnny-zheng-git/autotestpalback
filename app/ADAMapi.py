from flask_restplus import Api
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
def api(model):
    return Api( model,version='1.0', title='ADAM API',
          description='ADAM API', authorizations=authorizations, security='apikey')
