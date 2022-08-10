import os
from flask import Flask
from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'money.db'),
    )

    app.jinja_env.filters['datetime'] = datetime_format

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from .controllers import auth
    app.register_blueprint(auth.bp)

    from .controllers import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index') # so that url_for('index') and url_for('blog.index') are the same

    from .controllers import flow
    app.register_blueprint(flow.bp)

    from .controllers import profile
    app.register_blueprint(profile.bp)

    from .controllers import dashboard
    app.register_blueprint(dashboard.bp)

    return app


# custom datetime filter
def datetime_format(value, format="%d.%m.%Y"):
    value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return value.strftime(format)