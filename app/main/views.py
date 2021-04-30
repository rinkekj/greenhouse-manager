import os
from flask import Blueprint, render_template, send_file, Flask, request, redirect, url_for
from app import db, dprint, printSQL, getShortID
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
from flask_login import current_user, login_required
from app.main.forms import PlantTable
from datetime import date
import phonenumbers
from app.models import (
    Family,
    Genus,
    Species,
    Variety,
    Plant,
    Supplier,
    Item,
    Contact,
    Sales
)

main = Blueprint('main', __name__)

@main.route('/favicon.ico')
def favicon():
    return send_file('static/images/favicon.ico',
                     mimetype='image/vnd.microsoft.icon')

@main.route('/')
def index():

    if current_user.is_authenticated:
        return render_template('main/index.html')
    elif current_user.is_anonymous:
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('account.login'))



@main.route('/plant-inventory')
@login_required
def plant_inventory():
    dprint(current_user.is_admin())
    plants = []
    for p in Plant.query.all():
        plants.append( dict(fullName=p.fullName(),
                            sku=p.sku,
                            size=p.size,
                            quantity=p.quantity,
                            price=p.price,
                            supplier=p.supplierName(),
                            date_received=p.dateRec(), ))

    table = PlantTable(items=plants)
    return render_template('main/plant-inventory.html', table=table)

@main.route('/inventory')
@login_required
def inventory():
    items = []
    types = ['Plants','Supplies']
    for i in Item.query.all():
        dprint(i)
        if i.living == 'True':
            items.append(dict( name=i.shortName(),
                         sku=i.sku,
                         quantity=i.quantity,
                         price=i.price,
                         supplier=i.supplierName(),
                         date_received=i.dateRec(),
                         type = types[0],
                         supplierID = i.supplier(),
                         location = i.location,
                         ))
        else:
            items.append(dict( name=i.getName(),
                         sku=i.sku,
                         quantity=i.quantity,
                         price=i.price,
                         supplier=i.supplierName(),
                         date_received=i.dateRec(),
                         type = types[1],
                         supplierID = i.supplier(),
                         location = i.location,
                         ))

    return render_template('main/inventory.html', items=items, types=types)

@main.route('/inventory/items')
@login_required
def inventory_item():
    items = []
    for i in Item.query.all():
        if i.living == False:
            items.append(dict( name=i.name,
                         sku=i.sku,
                         quantity=i.quantity,
                         price=i.price,
                         supplier=i.supplierName(),
                         date_received=i.dateRec(),
                         supplierID = i.supplier()
                         ))

    return render_template('main/inventory-items.html', items=items)


#################################
# /species-database
# View taxonomic information
#
@main.route('/species-database')
@login_required
def speciesDB():

    families = db.session.query(Family).all()

    plantQu = db.session.query(Species, Genus, Family)\
        .join(Genus, Genus.id == Species.genus)\
        .join(Family, Family.id == Genus.family)

    varieties = {}
    for i in db.session.query(Variety).all():
        varieties[i.species] = i.name

    return render_template('plants/species-db.html',
                           plants=plantQu.all(),
                           families=families,
                           varieties=varieties)

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():

    return render_template('customer/checkout.html')


@main.route('/customers')
@login_required
def customers():
    """View all registered customers."""
    customers = Contact.query.all()
    phoneList = {}
    for i in customers:
        try:
            x = phonenumbers.parse(str(i.phone), "US")
        except:
            dprint('No phone')
        else:
            phoneList[i.id] = phonenumbers.format_number(
                x, phonenumbers.PhoneNumberFormat.NATIONAL)
    return render_template('customer/customer_list.html',
                           customers=customers,
                           phone=phoneList)


@main.route('/checkout/<customerID>', methods=['GET', 'POST'])
@login_required
def checkout2( customerID ):
    transactionID = getShortID()
    items = {}
    for i in Item.query.all():
        if i.quantity != 0:
            if i.living == True:
                items[ i.sku ] = {
                            'name' : i.shortName(),
                            'sku' : i.sku,
                            'quantity' : i.quantity,
                            'price' : i.price,
                            'type' : 'Plants',
                            }
            else:
                items[ i.sku ] = { 
                            'name' : i.name,
                            'sku' : i.sku,
                            'quantity' : i.quantity,
                            'price' : i.price,
                            'type' : 'Supplies',
                            }

    if request.method == "POST":

        dprint(dir(request.form))
        dprint(request.form.values())
        #for k in request.form.values():
        for i in request.form.to_dict():
            dprint(i, request.form[i])
            if request.form[i].isnumeric():
                cart = Sales(
                    id = transactionID,
                    date = date.today(),
                    customer = customerID,
                    item = i,
                    qty = request.form[i],
                    salePrice = items[i].price,
                    )
                db.session.add(cart)
                merch = Item.query.filter_by(sku=i).first()
                merch.updateQty( -int(request.form[i]) )
                db.session.commit()
                return redirect(url_for('main.receipt', saleID=cart.id,  ))
            else:
                break
    return render_template('main/checkout.html',items=items, types=types)

@main.route('/receipt/<saleID>', methods=['GET', 'POST'])
@login_required
def receipt(saleID):
    # Generate a receipt
    # Format as 60-char rows, like what could be sent to a standard receipt printer
    purchases = Sales.query.filter_by(id=saleID).all()
    sum = 0
    lines = []
    lines.append('{0:^60}'.format('University Greenhouse'))
    lines.append('{0:^60}'.format('2113 University Dr.'))
    lines.append('{0:^60}'.format('Rochester Hills, MI 48319'))
    lines.append('{0:^60}'.format('+1 (586) 321-4114'))
    lines.append('{0:-^60}'.format(''))
    lines.append('{:.<30}{:.>30}'.format('Transaction ID', saleID))
    lines.append('{:.<30}{:.>30}'.format('Cashier', current_user.first_name))
    lines.append('{:.<30}{:.>30}'.format('Date',date.today().strftime('%Y-%m-%d') ))
    lines.append('{0:-^60}'.format(''))

    for i in purchases:
        item = Item.query.filter_by(sku=i.item).scalar()
        itemCost = (int(i.qty) * i.salePrice)
        itemDetails = '[{}]  {}'.format( i.item, item.getName() )
        costBreakdown = '<{} @ ${}>{:>10}'.format( i.qty, i.salePrice, '$'+str(itemCost))
        lines.append('{:<30}{:>30}'.format( itemDetails, costBreakdown ))
        sum += itemCost
    grandTotal = '{}{:>10}'.format('Total', '$'+str(sum))
    lines.append('{0:^60}'.format(''))
    lines.append('{0:>60}'.format(grandTotal))
    lines.append('{0:-^60}'.format(''))
    lines.append('{0:^60}'.format('-End of Sale-'))

    return render_template('main/receipt.html', lines=lines)


@main.route('/suppliers', methods=['GET', 'POST'])
@login_required
def supplier_list():

    companies = db.session.query(Supplier).all()

    return render_template('main/suppliers.html', companies=companies)


@main.route('/suppliers/<supID>', methods=['GET', 'POST'])
@login_required
def vcard(supID):
    company = Supplier.query.filter_by(id=supID).first()
    contact = Contact.query.filter_by(id=company.contact).first()
    phone = phonenumbers.parse(str(contact.phone), "US")
    phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return render_template('main/vcard.html', company=company, contact=contact, phone=phone)
