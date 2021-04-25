from flask_wtf import FlaskForm
from flask_table import Table, Col


class PlantTable(Table):
    fullName = Col('Species')
    sku = Col('SKU')
    size = Col('Pot size')
    quantity = Col('Qty')
    price = Col('Price')
    supplier = Col('Supplier')
    date_received = Col('Date received')
