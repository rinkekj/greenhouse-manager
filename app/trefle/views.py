import wtforms_json
import json
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from app.trefle.forms import CorrectionsForm
import shamrock
from shamrock import Shamrock

api = Shamrock('Yw9dZYtMjWDqe5SYEPcxB7vO7VHU3t08cC_T9vNKlDQ')
wtforms_json.init()

trefle = Blueprint('trefle', __name__)

jsonBody = {
    'notes': None,
    'source_type': None,
    'source_reference': None,
    'correction': {
        'scientific_name': None,
        'rank': None,
        'genus': None,
        'year': None,
        'author': None,
        'bibliography': None,
        'common_name': None,
        'observations': None,
        'planting_description': None,
        'planting_sowing_description': None,
        'duration': None,
        'flower_color': None,
        'flower_conspicuous': None,
        'foliage_color': None,
        'foliage_texture': None,
        'leaf_retention': None,
        'fruit_color': None,
        'fruit_conspicuous': None,
        'fruit_seed_persistence': None,
        'fruit_months': None,
        'bloom_months': None,
        'ground_humidity': None,
        'growth_form': None,
        'growth_habit': None,
        'growth_months': None,
        'growth_rate': None,
        'edible_part': None,
        'vegetable': None,
        'light': None,
        'atmospheric_humidity': None,
        'adapted_to_coarse_textured_soils': None,
        'adapted_to_fine_textured_soils': None,
        'adapted_to_medium_textured_soils': None,
        'anaerobic_tolerance': None,
        'average_height_unit': None,
        'average_height_value': None,
        'maximum_height_unit': None,
        'maximum_height_value': None,
        'planting_row_spacing_unit': None,
        'planting_row_spacing_value': None,
        'planting_spread_unit': None,
        'planting_spread_value': None,
        'planting_days_to_harvest': None,
        'maximum_precipitation_unit': None,
        'maximum_precipitation_value': None,
        'minimum_precipitation_unit': None,
        'minimum_precipitation_value': None,
        'minimum_root_depth_unit': None,
        'minimum_root_depth_value': None,
        'ph_maximum': None,
        'ph_minimum': None,
        'soil_nutriments': None,
        'soil_salinity': None,
        'minimum_temperature_deg_c': None,
        'maximum_temperature_deg_c': None,
        'soil_texture': None,
        'ligneous_type': None,
        'toxicity': None
    }
}


@trefle.route('/')
def index():
    return render_template('trefle/index.html')


@trefle.route('/about')
def about():
    return render_template('trefle/about.html')


@trefle.route('/report')
def report():

    return render_template('trefle/report.html')


@trefle.route('/corrections', methods=['GET', 'POST'])
def corrections():
    form = CorrectionsForm.from_json(jsonBody)
    #if form.validate_on_submit():
    fieldList = []
    correctionList = []

    for i in jsonBody:
        fieldList.append(i)

    for i in jsonBody['correction']:
        correctionList.append(i)

    if request.method == 'POST' and form.validate():

        for i in request.form:
            q = request.form.get(i).strip()
            if i != 'csrf_token' and i != 'submit':
                if i in correctionList:
                    if q is not "" and not q.__contains__(
                            'empty') and q is not None:
                        jsonBody['correction'][i] = request.form.get(i)

                if i in fieldList:
                    if q is not "" and not q.__contains__('empty'):
                        jsonBody[i] = request.form.get(i)

        json2 = {}
        for i in jsonBody:
            if i in fieldList:
                if jsonBody[i] is not None and jsonBody[
                        i] is not 'null' and i is not 'correction':
                    json2[i] = jsonBody[i]

        json2['correction'] = {}

        for i in jsonBody['correction']:
            if jsonBody['correction'][i] is not None and jsonBody[
                    'correction'][i] is not 'null':
                json2['correction'][i] = jsonBody['correction'][i]

        print(json.dumps(json2, indent=4))
        print(json.dumps(jsonBody, indent=4))
        return render_template('trefle/corrections2.html', result=jsonBody)
        #return redirect(url_for('trefle.corrections2', dat=dat))

    #for i in request.form.data:
    #print([i])
    jstr = json.dumps(form.data, indent=4)
    with open('data.txt', 'w') as outfile:
        json.dump(jstr, outfile)

    jstr2 = json.dumps(form.patch_data, indent=4)
    with open('data2.txt', 'w') as outfile:
        json.dump(jstr2, outfile)
    return render_template('trefle/corrections.html', form=form)

    #print(api.corrections("ficus-lyrata", json2))
    print(api.corrections())


@trefle.route('/corrections2', methods=['GET', 'POST'])
def corrections2():
    print(request.form)
    #   jstr = json.dumps(request.data, indent=4)
    #   with open('data.txt', 'w') as outfile:
    #       json.dump(jstr, outfile)
    #   jstr2 = json.dumps(request.values, indent=4)
    #   with open('data2.txt', 'w') as outfile:
    #       json.dump(jstr2, outfile)
    return render_template('trefle/corrections2.html',
                           result=request.form.items)
