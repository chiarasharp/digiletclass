from flask import Flask
from flask import render_template, request, abort
from datetime import datetime
from .utils import parse_orgs, parse_people, parse_places
from . import app
from flask import redirect, url_for

ENTITY_CONFIG = {
    'orgs': {
        'parser': parse_orgs,
        'title': 'Organizzazioni',
    },
    'people': {
        'parser': parse_people,
        'title': 'Persone',
    },
    'places': {
        'parser': parse_places,
        'title': 'Luoghi',
    }
}

TYPE_MAP = {
    'library': 'Biblioteca', 'abbey': 'Abbazia', 'archdiocese': 'Arcidiocesi', 'church': 'Chiesa', 'tower': 'Torre',
    'monastery': 'Monastero', 'congregation': 'Congregazione', 'academy': 'Accademia', 'gallery': 'Galleria',
    'villa': 'Villa', 'university': 'Università', 'board': 'Collegio', 'reign': 'Regno', 'family': 'Famiglia',
    'institution': 'Istituzione', 'archive': 'Archivio', 'cathedral': 'Cattedrale', 'hospital': 'Ospedale',
    'convent': 'Convento', 'college': 'Collegio', 'basilica': 'Basilica', 'diocese': 'Diocesi',
    'seminary': 'Seminario', 'cemetery': 'Cimitero', 'rectory': 'Rettoria', 'hermitage': 'Eremo',
    'priory': 'Priorato', 'chapel': 'Cappella', 'shrine': 'Santuario', 'orphanage': 'Orfanotrofio',
    'settlement': 'Insediamento', 'source': 'Fonte', 'event': 'Evento', 'place': 'Luogo', 'duchy': 'Ducato',
    'religious-order': 'Ordine religioso', 'sanctuary': 'Santuario', 'none': 'Sconosciuto',
    'geonames': 'GeoNames', 'institute': 'Istituto', 'theatre': 'Teatro', 'castle': 'Castello',
    'abbazia': 'Abbazia', 'ospedale': 'Ospedale', 'biblioteca': 'Biblioteca', 'università': 'Università',
    'chiesa': 'Chiesa', 'monastero': 'Monastero', 'congregazione': 'Congregazione', 'galleria': 'Galleria',
    'santuario': 'Santuario', 'scuola': 'Scuola', 'museo': 'Museo', 'archivio': 'Archivio',
    'oratorio': 'Oratorio', 'parrocchia': 'Parrocchia', 'cattedrale': 'Cattedrale', 'basilica': 'Basilica',
    'diocesi': 'Diocesi', 'seminario': 'Seminario', 'collegio': 'Collegio', 'cimitero': 'Cimitero',
    'convento': 'Convento', 'rettoria': 'Rettoria', 'eremo': 'Eremo', 'priorato': 'Priorato',
    'cappella': 'Cappella', 'orfanotrofio': 'Orfanotrofio', 'altro': 'Altro',
    'places': {
        'settlement': 'Insediamento',
        'country': 'Nazione',
        'region': 'Regione',
        'city': 'Città',
        'province': 'Provincia',
        'land': 'Territorio',
        'populatedPlace': 'Luogo Abitato',
        'continent': 'Continente',
        'park': 'Parco',
        'nation': 'Nazione',
        'state': 'Stato',
        'island': 'Isola',
        'river': 'Fiume',
        'mountain': 'Montagna',
        'sea': 'Mare',
        'bay': 'Baia',
        'hill': 'Collina',
        'lake': 'Lago',
        'valley': 'Valle',
        'forest': 'Foresta',
        'peninsula': 'Penisola',
        'cape': 'Capo',
        'plain': 'Pianura',
        'desert': 'Deserto'
    }
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/entities')
def entities():
    return render_template('entities.html')

def get_pagination_window(page, total_pages, window=7):
    if total_pages <= window:
        return list(range(1, total_pages + 1))
    half = window // 2
    if page <= half + 1:
        return list(range(1, window)) + [None, total_pages]
    elif page >= total_pages - half:
        return [1, None] + list(range(total_pages - window + 2, total_pages + 1))
    else:
        return [1, None] + list(range(page - half + 1, page + half)) + [None, total_pages]

@app.route('/entities/<string:entity_type>')
def entities_list(entity_type):
    if entity_type not in ENTITY_CONFIG:
        abort(404)
    
    config = ENTITY_CONFIG[entity_type]
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    all_data = config['parser']()
    
    if entity_type == 'orgs':
        for org in all_data:
            if not org.get('type'):
                org['type'] = 'none'
    
    total = len(all_data)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = all_data[start:end]
    total_pages = int((total + per_page - 1) / per_page)
    pagination_window = get_pagination_window(page, total_pages)
    
    return render_template(
        'entities_list.html',
        items=paginated_data,
        all_items=all_data,
        item_type=entity_type,
        title=config['title'],
        type_map=TYPE_MAP if entity_type == 'orgs' else {},
        page=page,
        per_page=per_page,
        total=total,
        pagination_window=pagination_window
    )

@app.route('/orgs/<string:entity_id>/modal')
def org_modal(entity_id):
    data = parse_orgs()
    item = next((o for o in data if o['id'] == entity_id), None)
    if not item:
        return '', 404
    return render_template('_org_modal.html', org=item, type_map=TYPE_MAP)

@app.route('/people/<string:entity_id>/modal')
def person_modal(entity_id):
    data = parse_people()
    item = next((p for p in data if p['id'] == entity_id), None)
    if not item:
        return '', 404
    return render_template('_person_modal.html', person=item)

@app.route('/places/<string:entity_id>/modal')
def place_modal(entity_id):
    data = parse_places()
    item = next((p for p in data if p['id'] == entity_id), None)
    if not item:
        return '', 404
    return render_template('_place_modal.html', place=item)

@app.route('/modal/<entity_type>/<entity_id>')
def modal(entity_type, entity_id):
    if entity_type == 'orgs':
        return org_modal(entity_id)
    elif entity_type == 'people':
        return person_modal(entity_id)
    elif entity_type == 'places':
        return place_modal(entity_id)
    else:
        return '', 404
