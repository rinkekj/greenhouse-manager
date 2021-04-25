from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from app import db, dprint
from app.admin.forms import (
    NewEmployeeForm, 
    SupplierForm,
    ContactForm
)
from app.decorators import admin_required
from app.models import (
    Role,
    Employee,
    Contact,
    Supplier,
)
import phonenumbers

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    # Register new employee
    form = NewEmployeeForm()
    if form.validate_on_submit():
        user = Employee(role=form.role.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()), 'form-success')
    return render_template('admin/new_user.html', form=form)

@admin.route('/users')
@login_required
@admin_required
def registered_users():
    #View all registered users.
    users = Employee.query.all()
    roles = Role.query.all()
    return render_template('admin/registered_users.html', users=users, roles=roles)

@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    user = Employee.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    #Delete a user's account.
    if current_user.id == user_id:
        flash(
            'You cannot delete your own account. Please ask another '
            'administrator to do this.', 'error')
    else:
        user = Employee.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))

@admin.route('/add-supplier', methods=['GET', 'POST'])
@admin.route('/add-supplier/', methods=['GET', 'POST'])
def new_supplier():
    return edit_supplier(0)

@admin.route('/edit-supplier/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_supplier(id):
    #Add/Edit supplier info
    title = "New Supplier"
    form = SupplierForm()
    suppliersList = db.session.query(Supplier).all()
    choices = [(0, 'New')]
    for i in suppliersList:
        choices.append((i.id, i.name))
    form.addEdit.coerce = str
    form.addEdit.choices = choices

    if id is not None and id is not 0:
        title = "Edit "
        form.addEdit.default = id
        form.addEdit.data = id
        form.process()
        # Query supplier and contact
        # Pre-fill forms
        #form.addEdit.data = id

        supplierInfo = db.session.query(Supplier, Contact).join(
            Contact,
            Contact.id == Supplier.contact).filter(Supplier.id == id).first()

        form.state.data = supplierInfo.Supplier.state
        form.companyName.data = supplierInfo.Supplier.name
        form.address.data = supplierInfo.Supplier.address
        form.city.data = supplierInfo.Supplier.city
        form.zip.data = supplierInfo.Supplier.zip
        form.firstName.data = supplierInfo.Contact.first_name
        form.lastName.data = supplierInfo.Contact.last_name
        form.email.data = supplierInfo.Contact.email
        x = phonenumbers.parse(str(supplierInfo.Contact.phone), "US")
        form.phone.data = phonenumbers.format_number(
            x, phonenumbers.PhoneNumberFormat.NATIONAL)

    if form.validate_on_submit():

        # Add contact first so Supplier can use FK
        x = phonenumbers.parse(form.phone.data, "US")
        phoneNum = str(
            phonenumbers.format_number(
                x, phonenumbers.PhoneNumberFormat.NATIONAL))
        phoneNum = phoneNum.replace(" ", "")
        phoneNum = phoneNum.replace("(", "")
        phoneNum = phoneNum.replace(")", "")
        phoneNum = phoneNum.replace("-", "")

        contact = Contact(first_name=form.firstName.data,
                          last_name=form.lastName.data,
                          email=form.email.data,
                          phone=int(phoneNum))
        db.session.add(contact)
        db.session.commit()
        db.session.refresh(contact)

        company = Supplier(
            name=form.companyName.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data,
            contact=contact.id,
        )
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)

        flash('{} successfully added to contacts'.format(company.name),
              'form-success')
    return render_template('admin/new-supplier.html', form=form, title=title)



@admin.route('/add-contact', methods=['GET', 'POST'])
@admin.route('/add-contact/', methods=['GET', 'POST'])
def new_contact():
    return add_contact(0)

@admin.route('/add-contact/<id>', methods=['GET', 'POST'])
@login_required
def add_contact(id):
    # Add or update contact information
    title = "New Supplier"

    form = ContactForm()
    customerList = db.session.query(Supplier).all()
    choices = [(0, 'New')]
    for i in customerList:
        choices.append((i.id, i.name))
    form.addEdit.choices = choices

    if id is not None and id is not 0:
        title = "Edit Supplier"
        dprint(id)
        # Query supplier and contact
        # Pre-fill forms

        form.addEdit.data = id

        supplierInfo = db.session.query(Supplier, Contact).join(
            Contact,
            Contact.id == Supplier.contact).filter(Supplier.id == id).first()
        dprint(supplierInfo)

        form.state.data = supplierInfo.Supplier.state
        form.companyName.data = supplierInfo.Supplier.name
        form.address.data = supplierInfo.Supplier.address
        form.city.data = supplierInfo.Supplier.city
        form.zip.data = supplierInfo.Supplier.zip
        form.firstName.data = supplierInfo.Contact.first_name
        form.lastName.data = supplierInfo.Contact.last_name
        form.email.data = supplierInfo.Contact.email
        try:
            x = phonenumbers.parse(str(supplierInfo.Contact.phone), "US")
        except:
            dprint('No phone')
        else:
            form.phone.data = phonenumbers.format_number(
                x, phonenumbers.PhoneNumberFormat.NATIONAL)

    if form.validate_on_submit():
        # Add contact first so Supplier can use FK
        try:
            x = phonenumbers.parse(form.phone.data, "US")
        except:
            phoneNum = ''
            dprint('No phone number')
        else:
            phoneNum = str(
                phonenumbers.format_number(
                    x, phonenumbers.PhoneNumberFormat.NATIONAL))
            phoneNum = phoneNum.replace(" ", "")
            phoneNum = phoneNum.replace("(", "")
            phoneNum = phoneNum.replace(")", "")
            phoneNum = phoneNum.replace("-", "")

        contact = Contact(first_name=form.firstName.data,
                          last_name=form.lastName.data,
                          email=form.email.data,
                          phone=int(phoneNum))
        db.session.add(contact)
        db.session.commit()
        db.session.refresh(contact)

        company = Supplier(
            name=form.companyName.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data,
            contact=contact.id,
        )
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)

        flash('{} successfully added to contacts'.format(company.name),
              'form-success')
    return render_template('admin/new-supplier.html', form=form, title=title)


@admin.route('/customers')
@login_required
@admin_required
def customers():
    # View all registered customers.
    customers = Contact.query.all()
    phone = {}
    for i in customers:
        try:
            x = i.printNum()
        except:
            y = ''
        else:
            y = i.printNum()
        phone[i.id] = y 
    return render_template('admin/customer_list.html',
                           customers=customers,
                           phone=phone)


@admin.route('/edit-customer/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_customer(id):
    # destructive
    customer = Contact.query.filter_by(id=id).one()
    form = ContactForm(obj=customer)
    form.populate_obj(customer)

    if request.method == 'POST':
        
        form.phone.data = customer.parseNum(form.phone.data)
        form.populate_obj(customer)
        db.session.commit()
        flash('{} successfully updated'.format(customer.fullName()),'form-success')

    return render_template('admin/edit-customer.html',form=form, customer=customer)