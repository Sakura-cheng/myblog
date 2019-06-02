from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app
from flask_login import login_required
from myblog.extensions import db
from myblog.models import Post, Category
from myblog.forms import PostForm
from myblog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/manager')
@login_required
def manager():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('admin/manager.html', pagination=pagination, posts=posts)


@admin_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        category = Category.query.get(form.category.data)
        body = form.body.data
        post = Post(title=title, category=category, body=body)
        db.session.add(post)
        db.session.commit()
        flash('发表成功')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功' + str(post_id))
    return redirect_back()


@admin_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('blog.show_post', post_id=post_id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/new_post.html', form=form)
