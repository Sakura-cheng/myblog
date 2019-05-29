from flask import Blueprint, render_template, request, current_app
from myblog.models import Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/blogs.html', pagination=pagination, posts=posts)


@blog_bp.route('/thinking')
def thinking():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/thinkings.html', posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)
