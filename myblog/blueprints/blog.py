from flask import Blueprint

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    return '<h1>Hello, world!</h1>'
