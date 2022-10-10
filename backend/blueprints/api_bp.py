from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

app = Blueprint('api_bp', __name__,
                        template_folder='templates')

@app.route('/api')
def test():
    try:
        return "API"
    except TemplateNotFound:
        abort(404)