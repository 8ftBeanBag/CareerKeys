from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

app = Blueprint('main_bp', __name__,
                        template_folder='../templates')

@app.route('/', defaults={'page': 'index'})
@app.route('/<page>')
def get_page(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)


@app.route('/test')
def test():
    try:
        return "Tet"
    except TemplateNotFound:
        abort(404)