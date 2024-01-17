import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import request
from flask_babel import Babel
from flask_babel import lazy_gettext as _l

def get_locale():
    return os.environ.get('LANGUAGE') or request.accept_languages.best_match(app.config['LANGUAGES'])


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.preservation_planning import bp as pp_bp
    app.register_blueprint(pp_bp)

    from app.data_management import bp as dm_bp
    app.register_blueprint(dm_bp)

    if not app.debug and not app.testing:
        pass

    return app

from app import models