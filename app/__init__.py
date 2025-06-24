from flask import Flask
from .utils import format_iso_date, format_year

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.filters['format_date'] = format_iso_date
app.jinja_env.filters['year'] = format_year

# from .views import main_bp  # Removed: main_bp does not exist
