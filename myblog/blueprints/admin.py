from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required
from myblog.extensions import db
from myblog.models import Post, Category
from myblog.forms import PostForm

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/manager')
@login_required
def manager():
    return render_template('admin/manager.html')


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
