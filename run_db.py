from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from app.common import create_app, db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()


# >python manage.py db init
# >python manage.py db migrate
# >python manage.py db upgrade