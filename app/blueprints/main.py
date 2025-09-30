from flask import Blueprint, render_template, request, abort
from datetime import datetime

main_bp = Blueprint('main', __name__)

def get_news_data():
    """Return news data to avoid duplication across routes"""
    return [
        {
            'id': 'notte-ricercatori-2025',
            'title': 'Notte dei Ricercatori 2025',
            'date': '26 settembre 2025',
            'summary': 'Laboratorio "Dalla carta ai pixel e dall\'inchiostro al digitale. Alla scoperta delle lettere antiche della Biblioteca Classense".',
            'image': '/static/news/notte.png',
            'content': '''
            <p><strong>Laboratorio:</strong> "Dalla carta ai pixel e dall'inchiostro al digitale. Alla scoperta delle lettere antiche della Biblioteca Classense"</p>
            <p><strong>A cura di:</strong> Fiammetta Sabba, Bianca Sorbara, Chiara Manca, Francesca Fano (DBC – Unibo)</p>
            <p>All'interno delle iniziative realizzate per la Notte Europea dei Ricercatori 2025, il LUDI propone alcune attività laboratoriali per avvicinare il pubblico alla scoperta di lettere manoscritte antiche conservate presso la Biblioteca Classense di Ravenna e per mostrare le potenzialità offerte dagli strumenti digitali per la fruizione e la valorizzazione di tale patrimonio.
La proposta prende spunto dal progetto PNRR DigiLet Class (Digitizing Letters of Classense Library), attualmente in corso di svolgimento. Attraverso alcune copie di lettere settecentesche appartenenti al carteggio Canneti-Fiacchi, si potranno svolgere prove di lettura, di piegatura delle lettere e di scrittura con calamaio. A gruppi, i partecipanti potranno condurre anche una "caccia al tesoro" alla ricerca di vari elementi presenti nel testo, come luoghi, personaggi e opere.
In aggiunta, tramite una postazione dotata di computer, verranno mostrate le tecniche informatiche che consentono di trasformare la lettera fisica in lettera digitale tramite marcatura XML, e sarà possibile visionare e provare l'edizione digitale del carteggio.</p>
            ''',
            'url': 'https://www.nottedeiricercatori-society.eu/eventi/dalla-carta-ai-pixel-e-dallinchiostro-al-digitale-alla-scoperta-delle-lettere-antiche-della'
        },
        {
            'id': 'giornate-changes-2025',
            'title': 'Giornate DOORS of CHANGES 2025',
            'date': '16-19 ottobre 2025',
            'summary': 'Giornate di divulgazione promosse da Changes con mostra bibliografica temporanea delle lettere del carteggio Canneti-Fiacchi presso la Biblioteca Classense di Ravenna.',
            'content': '''
            <p>Durante le giornate di divulgazione promosse da Changes verrà presentata al pubblico una mostra bibliografica temporanea delle lettere del carteggio Canneti-Fiacchi presso la Biblioteca Classense di Ravenna.</p>
            <p>Un'occasione unica per scoprire dal vivo i documenti storici che sono alla base dell'edizione digitale DigiLetClass.</p>
            ''',
            'url': 'https://www.fondazionechanges.org/iniziative/mostra-temporanea-dellepistolario-tra-pietro-canneti-e-mariangelo-fiacchi-della-biblioteca-classense-di-ravenna/'
        },
        {
            'id': 'pubblicazione-atti-convegno',
            'title': 'Pubblicati gli atti del convegno "Epistolari classensi tra edizione e digitalizzazione"',
            'date': '2025',
            'summary': 'È disponibile il volume che raccoglie gli atti della giornata di studio del 9 dicembre 2024 presso la Biblioteca Classense di Ravenna.',
            'image': '/static/news/atti.png',
            'content': '''
            <p>È ora disponibile il volume <strong>"Epistolari classensi tra edizione e digitalizzazione"</strong>, a cura di Fiammetta Sabba con la collaborazione redazionale di Bianca Sorbara, pubblicato da Ledizioni nel 2025.</p>

            <p>Il volume raccoglie gli atti della giornata di studio tenutasi il <strong>9 dicembre 2024</strong> presso la Biblioteca Classense di Ravenna, presentando i risultati del progetto di ricerca DigiLetClass e offrendo una panoramica completa del lavoro di digitalizzazione e valorizzazione del carteggio Canneti-Fiacchi.</p>

            <p>I contributi scientifici illustrano le metodologie innovative applicate alla trascrizione, codifica TEI e creazione dell'edizione digitale, rappresentando un importante punto di riferimento per progetti simili nel campo delle digital humanities.</p>

            <p>Il testo è disponibile sia in formato cartaceo che in <strong>accesso aperto</strong> (Open Access), garantendo la massima diffusione dei risultati della ricerca.</p>
            ''',
            'url': 'https://www.ledizioni.it/prodotto/epistolari-classensi-tra-edizione-e-digitalizzazione/'
        }
    ]

@main_bp.route("/")
def home():
    # Get recent news for homepage preview (first 3 items)
    recent_news = get_news_data()[:3]
    return render_template("home.html", recent_news=recent_news)

@main_bp.route("/about/")
def about():
    return render_template("about.html")

@main_bp.route("/contact/")
def contact():
    return render_template("contact.html")

@main_bp.route('/entities')
def entities():
    return render_template('entities.html')

@main_bp.route('/entities/<string:entity_type>')
def entities_list(entity_type):
    from app.utils import parse_orgs, parse_people, parse_places, filter_entities_by_search
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
            'desert': 'Deserto',
            'ancient-settlement': 'Insediamento antico',
            'monastic-site': 'Sito monastico',
            'ancient-region': 'Regione antica',
            'historic-region': 'Regione storica',
            'stream': 'Torrente'
        }
    }
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
    if entity_type not in ENTITY_CONFIG:
        abort(404)
    config = ENTITY_CONFIG[entity_type]
    all_data = config['parser']()
    if entity_type == 'orgs':
        for item in all_data:
            if not item.get('type'):
                item['type'] = 'none'
    all_data = sorted(all_data, key=lambda x: x.get('name', '').lower())
    selected_type = request.args.get('type', 'all')
    search_query = request.args.get('search', '')
    filtered_data = all_data
    org_types = []
    place_types = []
    if entity_type == 'orgs':
        org_types = sorted(list(set(org.get('type', 'none') for org in all_data)))
        if selected_type != 'all':
            filtered_data = [org for org in all_data if org.get('type', 'none') == selected_type]
        filtered_data = filter_entities_by_search(filtered_data, 'orgs', search_query)
        country = request.args.get('country', '').strip().upper()
        settlement = request.args.get('settlement', '').strip().lower()
        if country:
            filtered_data = [org for org in filtered_data if org.get('location') and org['location'].get('country') and org['location'].get('country', '').upper() == country]
        if settlement:
            filtered_data = [org for org in filtered_data if org.get('location') and org['location'].get('settlement') and org['location'].get('settlement', '').lower() == settlement]
    elif entity_type == 'places':
        place_types = sorted(list(set(p.get('type', 'none') for p in all_data)))
        if selected_type != 'all':
            filtered_data = [p for p in all_data if p.get('type', 'none') == selected_type]
        filtered_data = filter_entities_by_search(filtered_data, 'places', search_query)
        country = request.args.get('country', '').strip().upper()
        settlement = request.args.get('settlement', '').strip().lower()
        if country:
            filtered_data = [p for p in filtered_data if p.get('location') and p['location'].get('country') and p['location'].get('country', '').upper() == country]
        if settlement:
            filtered_data = [p for p in filtered_data if p.get('location') and p['location'].get('settlement') and p['location'].get('settlement', '').lower() == settlement]
    elif entity_type == 'people':
        filtered_data = filter_entities_by_search(filtered_data, 'people', search_query)
        sex = request.args.get('sex', '').strip().lower()
        birth_from = request.args.get('birth_from', '').strip()
        birth_to = request.args.get('birth_to', '').strip()
        if sex:
            filtered_data = [person for person in filtered_data if person.get('sex', '').lower() == sex]
        if birth_from:
            try:
                birth_from_year = int(birth_from)
                filtered_data = [person for person in filtered_data if person.get('birth') and person['birth'][:4].isdigit() and int(person['birth'][:4]) >= birth_from_year]
            except ValueError:
                pass
        if birth_to:
            try:
                birth_to_year = int(birth_to)
                filtered_data = [person for person in filtered_data if person.get('birth') and person['birth'][:4].isdigit() and int(person['birth'][:4]) <= birth_to_year]
            except ValueError:
                pass
    page = request.args.get('page', 1, type=int)
    per_page = 12
    total = len(filtered_data)
    total_pages = int((total + per_page - 1) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = filtered_data[start:end]
    pagination_window = get_pagination_window(page, total_pages)
    type_map_for_template = {}
    if entity_type == 'orgs':
        type_map_for_template = TYPE_MAP
    elif entity_type == 'places':
        type_map_for_template = TYPE_MAP.get('places', {})
    return render_template(
        'entities_list.html',
        items=paginated_items,
        item_type=entity_type,
        title=config['title'],
        org_types=org_types,
        place_types=place_types,
        selected_type=selected_type,
        type_map=type_map_for_template,
        page=page,
        per_page=per_page,
        total=total,
        pagination_window=pagination_window
    )

@main_bp.route('/orgs/<string:entity_id>/modal')
def org_modal(entity_id):
    return render_template('_org_modal.html', org={}, type_map={})

@main_bp.route('/people/<string:entity_id>/modal')
def person_modal(entity_id):
    return render_template('_person_modal.html', person={})

@main_bp.route('/places/<string:entity_id>/modal')
def place_modal(entity_id):
    return render_template('_place_modal.html', place={}, type_map={})

@main_bp.route('/modal/<entity_type>/<entity_id>')
def modal(entity_type, entity_id):
    from app.utils import parse_orgs, parse_people, parse_places
    from flask import abort
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
            'desert': 'Deserto',
            'ancient-settlement': 'Insediamento antico',
            'monastic-site': 'Sito monastico',
            'ancient-region': 'Regione antica',
            'historic-region': 'Regione storica',
            'stream': 'Torrente'
        }
    }
    if entity_type == 'orgs':
        data = parse_orgs()
        item = next((o for o in data if o['id'] == entity_id), None)
        if not item:
            return '', 404
        return render_template('_org_modal.html', org=item, type_map=TYPE_MAP)
    elif entity_type == 'people':
        data = parse_people()
        item = next((p for p in data if p['id'] == entity_id), None)
        if not item:
            return '', 404
        return render_template('_person_modal.html', person=item)
    elif entity_type == 'places':
        data = parse_places()
        item = next((p for p in data if p['id'] == entity_id), None)
        if not item:
            return '', 404
        return render_template('_place_modal.html', place=item, type_map=TYPE_MAP.get('places', {}))
    else:
        return '', 404

@main_bp.route('/methodology')
def methodology():
    return render_template('methodology.html')

@main_bp.route('/project')
def project():
    return render_template('project.html')

@main_bp.route('/news')
def news():
    entries = get_news_data()
    return render_template('news.html', entries=entries)

@main_bp.route('/news/<news_id>')
def news_detail(news_id):
    entries = get_news_data()
    item = next((entry for entry in entries if entry['id'] == news_id), None)
    if not item:
        abort(404)
    return render_template('news_detail.html', item=item)
