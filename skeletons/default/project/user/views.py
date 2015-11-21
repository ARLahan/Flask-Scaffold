# user/views.py
"""User views."""

from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask.ext.login import login_user, logout_user, login_required

from .. import bcrypt, db
from .models import User
from .forms import LoginForm, RegisterForm

# User blueprint
user_blueprint = Blueprint('user', __name__,
                           url_prefix='/user',
                           static_folder='static',
                           static_url_path='/user/static',
                           template_folder='templates')


# User blueprint routes
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """User register view."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for('.dashboard'))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """User login view."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('.dashboard'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    """User logout view."""
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/')
@user_blueprint.route('/dashboard')
@login_required
def members():
    """User area view."""
    return render_template('user/dashboard.html')
