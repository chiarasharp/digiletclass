from flask import Flask, render_template
from .utils import format_iso_date, format_year
from .blueprints.main import main_bp

def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)

    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.filters['format_date'] = format_iso_date
    app.jinja_env.filters['year'] = format_year

    app.register_blueprint(main_bp)

    # Error handlers
    def render_error(error, template, code):
        return render_template(template), code

    @app.errorhandler(404)
    def not_found_error(error):
        return render_error(error, "404.html", 404)

    @app.errorhandler(500)
    def internal_error(error):
        return render_error(error, "500.html", 500)

    return app
