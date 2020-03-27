from app.common import create_app
from app.user.urls import user_mold
from app.interfacetest.urls import  project_mold


app = create_app()
app.register_blueprint(user_mold,url_prefix='/user')
app.register_blueprint(project_mold, url_prefix='/project')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
