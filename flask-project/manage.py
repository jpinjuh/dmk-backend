from flask_script import Manager, Server
from flask_alembic.cli.script import manager as alembic_manager

from FlaskProject import create_app, environments, models, scripts
from FlaskProject.db import db


if __name__ == '__main__':
    manager = Manager(create_app)
    manager.add_command('runserver', Server(
        host='0.0.0.0', port=5000, threaded=True))

    alembic_manager.add_command('seed', scripts.Seed)
    alembic_manager.add_command('truncate', scripts.Truncate)

    manager.add_command('db', alembic_manager)

    manager.add_command('routes', scripts.Routes)

    manager.add_option(
        '-e', '--environment',
        default='development',
        choices=environments.keys(),
        dest='config_environment',
        required=False,
    )

    # Add some more stuff to manager shell so we don't need to import that
    # manually every time
    @manager.shell
    def make_shell_context():
        context = dict(
            app=create_app,
            db=db,
            models=models,
        )
        context.update(vars(models))
        return context

    manager.run()


