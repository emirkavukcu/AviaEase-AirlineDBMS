from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db  # Import create_app function and db object from your package

app = create_app()  # Create an app instance using the factory function
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
