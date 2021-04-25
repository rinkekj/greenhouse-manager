from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import db, dprint, printSQL
from app.account.forms import LoginForm
from app.models import Employee

account = Blueprint('account', __name__)

@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        printSQL()
        if user is not None and user.password_hash is not None:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                flash('Successfully logged in', 'success')
                return redirect( url_for('main.index'))
            else:
                flash('Invalid email or password.', 'error')
    return render_template('account/login.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
