from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    StringField,
    SubmitField,
    RadioField,
    FieldList,
    FormField,
    SelectField,
    IntegerField,
    DecimalField,
    BooleanField,
)
from wtforms.fields.html5 import (
    SearchField,
    DateField,
)
from wtforms.validators import (
    EqualTo,
    InputRequired,
    Length,
    Optional,
    NumberRange,
)
from wtforms.widgets.html5 import (
    DateInput, )
from wtforms.widgets import (
    TextArea, )
from app import db
from app.models import (
    Family,
    Genus,
    Species,
    Variety,
    Plant,
    Supplier,
    WaterLog,
)

import sys
import decimal


class DollarField(DecimalField):
    def __init__(self,
                 label=None,
                 validators=None,
                 places=2,
                 rounding=None,
                 round_always=False,
                 **kwargs):
        super(DollarField, self).__init__(label=label,
                                          validators=validators,
                                          places=places,
                                          rounding=rounding,
                                          **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                newPrice = float(valuelist[0].strip('$').replace(',', ''))
                self.data = decimal.Decimal(newPrice)
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1')**self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(exp,
                                                       rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Not a valid decimal value'))


class PlantSearchForm(FlaskForm):
    plantName = SearchField('Search for plant',
                            validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Search')

class SelectForm(FlaskForm):
    plantInfo = RadioField('Species', validators=[InputRequired()], coerce=int)
    submit = SubmitField('Select')

    def number_of_results(self):
        return len(self.plantInfo.choices)

class TaxonForm(FlaskForm):
    family = SelectField()
    genus = SelectField()

class SpeciesForm(TaxonForm):
    species = StringField()

class VarietyForm(TaxonForm):
    species = SelectField()
    variety = StringField()

class plantForm(FlaskForm):
    family = SelectField(
        u'Family',
        id='family_select',
        choices=[('0', '------'),],
        coerce=int,
    )
    genus = SelectField(
        u'Genus',
        id='genus_select',
        choices=[('0', '------'),],
        coerce=int,
    )

    species = SelectField(
        u'Species',
        id='species_select',
        choices=[('0', '------')],
        coerce=int,
    )

    variety = SelectField(
        u'Variety',
        id='variety_select',
        choices=[('0', '------')],
        coerce=str,
    )
    
    substrate = SelectField(
        u'Substrate',
        id='substrate_select',
        choices=[('0', '------'),],
        coerce=int,
    )

    parent = SelectField(
        u'Parent',
        id='parent_select',
        choices=[('0', '------'),],
        coerce=str,
    )
    '''
    price = DollarField(u'Price',
                        round_always=True,
                        validators=[InputRequired(),])

    quantity = IntegerField(u'Quantity',
                            validators=[
                                InputRequired(),
                                NumberRange(min=1, max=500, message="Quantity can not be zero")
                            ])
    '''
    size = IntegerField(u'Pot size (in)',
                        validators=[
                            InputRequired(),
                            NumberRange(min=1, max=24, message="Please enter a valid size")
                        ])
    
    date_received = DateField(widget=DateInput(),
                              validators=[Optional(),],)
    submit = SubmitField('Submit')

    def plant_list(request, id):
        plant = db.session.query(Family)
        form = plantForm(request.POST, obj=plant)
        form.family.choices = [(f.id, f.name)
                               for f in Family.query.order_by('name')]

    #for entry in Species.query.filter_by(genus=genID).all():
    #	data[entry.id] = entry.name


class substrateForm(FlaskForm):
    name = StringField(u'Name', validators=[InputRequired(),])
    notes = StringField(u'Text', widget=TextArea(), validators=[InputRequired(),])

class plantInventoryForm(FlaskForm):
    sku = StringField()
    family = SelectField()
    genus = SelectField()
    species = SelectField()
    size = IntegerField()
    quantity = IntegerField('Quantity')
    supplier = SelectField('Supplier', )
    date_received = DateField(widget=DateInput())
    price = DollarField('Price',
                        round_always=True,
                        validators=[InputRequired(),])


class waterForm(FlaskForm):
    date = DateField(widget=DateInput())
    water = BooleanField()
    feed = BooleanField()
    notes = StringField(u'Text', widget=TextArea())
    submit = SubmitField('Submit')
