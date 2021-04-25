from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_rq import get_queue

from app import db
from app.register.forms import (LoginForm, RegistrationForm)
from app.models import Contact
from app.admin.forms import ContactForm
register = Blueprint('register', __name__)


@register.route('/')
def index():
    return render_template('customer/checkout.html')


@register.route('/returning', methods=['GET', 'POST'])
def returning():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Contact.query.filter_by(email=form.email.data).first()
        if customer is not None:
            return redirect(
                request.args.get('next') or url_for('register.manage'))
    return render_template('customer/login.html', form=form)


@register.route('/register', methods=['GET', 'POST'])
def registration():
    form = ContactForm()
    if form.validate_on_submit():
        customer = Contact(first_name=form.first_name.data,
                           last_name=form.last_name.data,
                           email=form.email.data,
                           phone=form.phone.data )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('register.manage'))
    return render_template('customer/register.html', form=form)
