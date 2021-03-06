from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.validators import Optional
from wtforms.fields import BooleanField, StringField, RadioField, SelectField, IntegerField, FloatField, SelectMultipleField, SubmitField
#import wtforms_json

#wtforms_json.init()


class CorrectionsForm(FlaskForm):
    notes = StringField('Notes', validators=[
        Optional(),
    ], default='TEST')
    source_type = RadioField(choices=[('external', 'external'),
                                      ('internal', 'internal')],
                             default=[
                                 'external',
                             ],
                             validators=[
                                 Optional(),
                             ])
    source_reference = StringField(validators=[
        Optional(),
    ])
    scientific_name = StringField(validators=[
        Optional(),
    ])
    rank = SelectField(choices=[('', ''),
                                ('species', 'species'), ('spp', 'ssp'),
                                ('var', 'var'), ('form', 'form'),
                                ('hybrid', 'hybrid'), ('subvar', 'subvar')],
                       validators=[
                           Optional(),
                       ])
    genus = StringField(validators=[
        Optional(),
    ])
    year = IntegerField(validators=[
        Optional(),
    ])
    author = StringField(validators=[
        Optional(),
    ])
    bibliography = StringField(validators=[
        Optional(),
    ])
    # Several values can be separated with "|"
    common_name = StringField(validators=[
        Optional(),
    ])
    observations = StringField(validators=[
        Optional(),
    ])
    planting_description = StringField(validators=[
        Optional(),
    ])
    planting_sowing_description = StringField(validators=[
        Optional(),
    ])
    duration = SelectField(choices=[('empty', ''), ('annual', 'annual'),
                                    ('biennial', 'biennial'),
                                    ('perennial', 'perennial')],
                           validators=[
                               Optional(),
                           ])
    flower_color = SelectField(choices=[('empty', ''), ('white', 'white'),
                                        ('red', 'red'), ('brown', 'brown'),
                                        ('orange', 'orange'),
                                        ('yellow', 'yellow'), ('lime', 'lime'),
                                        ('green', 'green'), ('cyan', 'cyan'),
                                        ('blue', 'blue'), ('purple', 'purple'),
                                        ('magenta', 'magenta'),
                                        ('grey', 'grey'), ('black', 'black')],
                               validators=[
                                   Optional(),
                               ])
    flower_conspicuous = BooleanField(validators=[
        Optional(),
    ])
    # Several values can be separated with "|"
    foliage_color = SelectMultipleField(choices=[('empty', ''),
                                                 ('white', 'white'),
                                                 ('red', 'red'),
                                                 ('brown', 'brown'),
                                                 ('orange', 'orange'),
                                                 ('yellow', 'yellow'),
                                                 ('lime', 'lime'),
                                                 ('green', 'green'),
                                                 ('cyan', 'cyan'),
                                                 ('blue', 'blue'),
                                                 ('purple', 'purple'),
                                                 ('magenta', 'magenta'),
                                                 ('grey', 'grey'),
                                                 ('black', 'black')],
                                        validators=[
                                            Optional(),
                                        ])
    foliage_texture = SelectField(choices=[('empty', ''), ('fine', 'fine'),
                                           ('medium', 'medium'),
                                           ('course', 'coarse')],
                                  validators=[
                                      Optional(),
                                  ])
    leaf_retention = BooleanField(validators=[
        Optional(),
    ])
    fruit_color = SelectMultipleField(choices=[('empty', ''),
                                               ('white', 'white'),
                                               ('red', 'red'),
                                               ('brown', 'brown'),
                                               ('orange', 'orange'),
                                               ('yellow', 'yellow'),
                                               ('lime', 'lime'),
                                               ('green', 'green'),
                                               ('cyan', 'cyan'),
                                               ('blue', 'blue'),
                                               ('purple', 'purple'),
                                               ('magenta', 'magenta'),
                                               ('grey', 'grey'),
                                               ('black', 'black')],
                                      validators=[
                                          Optional(),
                                      ])
    fruit_conspicuous = BooleanField(validators=[
        Optional(),
    ])
    fruit_seed_persistence = BooleanField(validators=[
        Optional(),
    ])
    # Several values can be separated with "|"
    fruit_months = SelectMultipleField(choices=[('jan', 'jan'), ('feb', 'feb'),
                                                ('mar', 'mar'), ('apr', 'apr'),
                                                ('may', 'may'), ('jun', 'jun'),
                                                ('jul', 'jul'), ('aug', 'aug'),
                                                ('sep', 'sep'), ('oct', 'oct'),
                                                ('nov', 'nov'),
                                                ('dec', 'dec')],
                                       validators=[
                                           Optional(),
                                       ])
    # Several values can be separated with "|"
    bloom_months = SelectMultipleField(choices=[('jan', 'jan'), ('feb', 'feb'),
                                                ('mar', 'mar'), ('apr', 'apr'),
                                                ('may', 'may'), ('jun', 'jun'),
                                                ('jul', 'jul'), ('aug', 'aug'),
                                                ('sep', 'sep'), ('oct', 'oct'),
                                                ('nov', 'nov'),
                                                ('dec', 'dec')],
                                       validators=[
                                           Optional(),
                                       ])
    # 0 (xerophile) to 10 (subaquatic)
    ground_humidity = IntegerField(validators=[
        Optional(),
    ])
    growth_form = StringField(validators=[
        Optional(),
    ])
    growth_habit = StringField(validators=[
        Optional(),
    ])
    # Several values can be separated with "|"
    growth_months = SelectMultipleField(choices=[
        ('jan', 'jan'), ('feb', 'feb'), ('mar', 'mar'), ('apr', 'apr'),
        ('may', 'may'), ('jun', 'jun'), ('jul', 'jul'), ('aug', 'aug'),
        ('sep', 'sep'), ('oct', 'oct'), ('nov', 'nov'), ('dec', 'dec')
    ],
                                        validators=[
                                            Optional(),
                                        ])
    growth_rate = StringField(validators=[
        Optional(),
    ])
    edible_part = SelectMultipleField(choices=[('roots', 'roots'),
                                               ('stems', 'stem'),
                                               ('leaves', 'leaves'),
                                               ('flowers', 'flowers'),
                                               ('fruits', 'fruits'),
                                               ('seeds', 'seeds')],
                                      validators=[
                                          Optional(),
                                      ])
    vegetable = BooleanField(validators=[
        Optional(),
    ])
    # scale from 0 (no light, <= 10 lux) to 10 (very intensive insolation, >= 100 000 lux)
    light = IntegerField(validators=[
        Optional(),
    ])
    atmospheric_humidity = IntegerField(validators=[
        Optional(),
    ])
    adapted_to_coarse_textured_soils = BooleanField(validators=[
        Optional(),
    ])
    adapted_to_fine_textured_soils = BooleanField(validators=[
        Optional(),
    ])
    adapted_to_medium_textured_soils = BooleanField(validators=[
        Optional(),
    ])
    anaerobic_tolerance = BooleanField(validators=[
        Optional(),
    ])
    average_height_unit = SelectField(choices=[('empty', ''), ('in', 'in'),
                                               ('ft', 'ft'), ('cm', 'cm'),
                                               ('m', 'm')],
                                      validators=[
                                          Optional(),
                                      ])
    average_height_value = FloatField(validators=[
        Optional(),
    ])
    maximum_height_unit = SelectField(choices=[('empty', ''), ('in', 'in'),
                                               ('ft', 'ft'), ('cm', 'cm'),
                                               ('m', 'm')],
                                      validators=[
                                          Optional(),
                                      ])
    maximum_height_value = FloatField(validators=[
        Optional(),
    ])
    planting_row_spacing_unit = SelectField(choices=[
        ('empty', ''), ('in', 'in'), ('ft', 'ft'), ('cm', 'cm'), ('m', 'm')
    ],
                                            validators=[
                                                Optional(),
                                            ])
    planting_row_spacing_value = FloatField(validators=[
        Optional(),
    ])
    planting_spread_unit = SelectField(choices=[('empty', ''), ('in', 'in'),
                                                ('ft', 'ft'), ('cm', 'cm'),
                                                ('m', 'm')],
                                       validators=[
                                           Optional(),
                                       ])
    planting_spread_value = FloatField(validators=[
        Optional(),
    ])
    planting_days_to_harvest = IntegerField(validators=[
        Optional(),
    ])
    maximum_precipitation_unit = SelectField(choices=[
        ('empty', ''), ('in', 'in'), ('ft', 'ft'), ('cm', 'cm'), ('m', 'm')
    ],
                                             validators=[
                                                 Optional(),
                                             ])
    maximum_precipitation_value = IntegerField(validators=[
        Optional(),
    ])
    minimum_precipitation_unit = SelectField(choices=[
        ('empty', ''), ('in', 'in'), ('ft', 'ft'), ('cm', 'cm'), ('m', 'm')
    ],
                                             validators=[
                                                 Optional(),
                                             ])
    minimum_precipitation_value = IntegerField(validators=[
        Optional(),
    ])
    minimum_root_depth_unit = SelectField(choices=[('empty', ''), ('in', 'in'),
                                                   ('ft', 'ft'), ('cm', 'cm'),
                                                   ('m', 'm')],
                                          validators=[
                                              Optional(),
                                          ])
    minimum_root_depth_value = IntegerField(validators=[
        Optional(),
    ])
    ph_maximum = FloatField('pH Maximum', validators=[
        Optional(),
    ])
    ph_minimum = FloatField('pH Minimum', validators=[
        Optional(),
    ])
    # Required quantity of nutriments in the soil, on a scale from 0 (oligotrophic) to 10 (hypereutrophic)
    soil_nutriments = IntegerField(validators=[
        Optional(),
    ])
    # Tolerance to salinity, on a scale from 0 (untolerant) to 10 (hyperhaline)
    soil_salinity = IntegerField(validators=[
        Optional(),
    ])
    # Degrees celcius
    minimum_temperature_deg_c = IntegerField(validators=[
        Optional(),
    ])
    # Degrees celcius
    maximum_temperature_deg_c = IntegerField(validators=[
        Optional(),
    ])
    # Required texture of the soil, on a scale from 0 (clay) to 10 (rock)
    soil_texture = IntegerField(validators=[
        Optional(),
    ])
    ligneous_type = SelectField(choices=[('empty', ''), ('liana', 'liana'),
                                         ('subshrub', 'subshrub'),
                                         ('shrub', 'shrub'), ('tree', 'tree'),
                                         ('parasite', 'parasite')],
                                validators=[
                                    Optional(),
                                ])
    toxicity = SelectField(choices=[('empty', ''), ('none', 'none'),
                                    ('low', 'low'), ('medium', 'medium'),
                                    ('high', 'high')],
                           validators=[
                               Optional(),
                           ])
    submit = SubmitField('Submit')
