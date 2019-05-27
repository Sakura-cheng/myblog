from flask import Blueprint, render_template
from myblog.models import Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/blogs.html', posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)
