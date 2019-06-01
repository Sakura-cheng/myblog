# 认证相关
from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user
from myblog.models import Admin
from myblog.forms import LoginForm
from myblog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('登录成功')
                return redirect_back()
            else:
                flash('账号或密码错误')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('登出成功')
    return redirect_back()
