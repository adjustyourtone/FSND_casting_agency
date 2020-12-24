from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, migrate

from app import api
from models import db

migrate = Migrate(api, db)
manager = Manager(api)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
