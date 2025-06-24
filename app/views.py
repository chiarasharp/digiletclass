from flask import Flask
from flask import render_template
from datetime import datetime
from .utils import parse_orgs
from . import app
from flask import redirect, url_for

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

@app.route('/entities/orgs')
def orgs():
    orgs_data = parse_orgs() 
    for org in orgs_data:
        if not org.get('type'):
            org['type'] = 'none'
    type_map = {
        'library': 'Biblioteca',
        'abbey': 'Abbazia',
        'archdiocese': 'Arcidiocesi',
        'church': 'Chiesa',
        'tower': 'Torre',
        'monastery': 'Monastero',
        'congregation': 'Congregazione',
        'academy': 'Accademia',
        'gallery': 'Galleria',
        'villa': 'Villa',
        'university': 'Università',
        'board': 'Collegio',
        'reign': 'Regno',
        'family': 'Famiglia',
        'institution': 'Istituzione',
        'archive': 'Archivio',
        'cathedral': 'Cattedrale',
        'hospital': 'Ospedale',
        'convent': 'Convento',
        'college': 'Collegio',
        'basilica': 'Basilica',
        'diocese': 'Diocesi',
        'seminary': 'Seminario',
        'cemetery': 'Cimitero',
        'rectory': 'Rettoria',
        'hermitage': 'Eremo',
        'priory': 'Priorato',
        'chapel': 'Cappella',
        'shrine': 'Santuario',
        'orphanage': 'Orfanotrofio',
        'settlement': 'Insediamento',
        'source': 'Fonte',
        'event': 'Evento',
        'place': 'Luogo',
        'duchy': 'Ducato',
        'religious-order': 'Ordine religioso',
        'sanctuary': 'Santuario',
        'none': 'Sconosciuto',
        'geonames': 'GeoNames',
        'institute': 'Istituto',
        'theatre': 'Teatro',
        'castle': 'Castello',
        'abbazia': 'Abbazia',
        'ospedale': 'Ospedale',
        'biblioteca': 'Biblioteca',
        'università': 'Università',
        'chiesa': 'Chiesa',
        'monastero': 'Monastero',
        'congregazione': 'Congregazione',
        'galleria': 'Galleria',
        'santuario': 'Santuario',
        'scuola': 'Scuola',
        'museo': 'Museo',
        'archivio': 'Archivio',
        'oratorio': 'Oratorio',
        'parrocchia': 'Parrocchia',
        'cattedrale': 'Cattedrale',
        'basilica': 'Basilica',
        'diocesi': 'Diocesi',
        'seminario': 'Seminario',
        'collegio': 'Collegio',
        'cimitero': 'Cimitero',
        'convento': 'Convento',
        'rettoria': 'Rettoria',
        'eremo': 'Eremo',
        'priorato': 'Priorato',
        'cappella': 'Cappella',
        'orfanotrofio': 'Orfanotrofio',
        'altro': 'Altro'
    }
    return render_template('orgs.html', orgs=orgs_data, type_map=type_map)

@app.route('/entities')
def entities():
    return render_template('entities.html')

@app.route('/org/<org_id>/modal')
def org_modal(org_id):
    orgs_data = parse_orgs()
    org = next((o for o in orgs_data if o['id'] == org_id), None)
    if not org:
        return '', 404
    type_map = {
        'library': 'Biblioteca',
        'abbey': 'Abbazia',
        'archdiocese': 'Arcidiocesi',
        'church': 'Chiesa',
        'tower': 'Torre',
        'monastery': 'Monastero',
        'congregation': 'Congregazione',
        'academy': 'Accademia',
        'gallery': 'Galleria',
        'villa': 'Villa',
        'university': 'Università',
        'board': 'Collegio',
        'reign': 'Regno',
        'family': 'Famiglia',
        'institution': 'Istituzione',
        'archive': 'Archivio',
        'cathedral': 'Cattedrale',
        'hospital': 'Ospedale',
        'convent': 'Convento',
        'college': 'Collegio',
        'basilica': 'Basilica',
        'diocese': 'Diocesi',
        'seminary': 'Seminario',
        'cemetery': 'Cimitero',
        'rectory': 'Rettoria',
        'hermitage': 'Eremo',
        'priory': 'Priorato',
        'chapel': 'Cappella',
        'shrine': 'Santuario',
        'orphanage': 'Orfanotrofio',
        'settlement': 'Insediamento',
        'source': 'Fonte',
        'event': 'Evento',
        'place': 'Luogo',
        'duchy': 'Ducato',
        'religious-order': 'Ordine religioso',
        'sanctuary': 'Santuario',
        'none': 'Sconosciuto',
        'geonames': 'GeoNames',
        'institute': 'Istituto',
        'theatre': 'Teatro',
        'castle': 'Castello',
        'abbazia': 'Abbazia',
        'ospedale': 'Ospedale',
        'biblioteca': 'Biblioteca',
        'università': 'Università',
        'chiesa': 'Chiesa',
        'monastero': 'Monastero',
        'congregazione': 'Congregazione',
        'galleria': 'Galleria',
        'santuario': 'Santuario',
        'scuola': 'Scuola',
        'museo': 'Museo',
        'archivio': 'Archivio',
        'oratorio': 'Oratorio',
        'parrocchia': 'Parrocchia',
        'cattedrale': 'Cattedrale',
        'basilica': 'Basilica',
        'diocesi': 'Diocesi',
        'seminario': 'Seminario',
        'collegio': 'Collegio',
        'cimitero': 'Cimitero',
        'convento': 'Convento',
        'rettoria': 'Rettoria',
        'eremo': 'Eremo',
        'priorato': 'Priorato',
        'cappella': 'Cappella',
        'orfanotrofio': 'Orfanotrofio',
        'altro': 'Altro'
    }
    return render_template('_org_modal.html', org=org, type_map=type_map)
