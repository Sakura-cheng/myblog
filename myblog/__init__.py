from flask import Flask, render_template
from myblog.settings import config
import os
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.blueprints.admin import admin_bp
from myblog.extensions import moment, db, ckeditor


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('myblog')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_errors(app)
    return app


def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/404.html'), 404
