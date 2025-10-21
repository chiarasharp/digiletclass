from flask import Blueprint, render_template, request, abort
from datetime import datetime
from app.utils import get_news_data, TYPE_MAP, get_pagination_window, parse_orgs, parse_people, parse_places, filter_entities_by_search

main_bp = Blueprint('main', __name__)

# Constants
ITEMS_PER_PAGE = 12
RECENT_NEWS_COUNT = 3
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

@main_bp.route("/")
def home():
    # Get recent news for homepage preview
    recent_news = get_news_data()[:RECENT_NEWS_COUNT]
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
    total = len(filtered_data)
    total_pages = int((total + ITEMS_PER_PAGE - 1) / ITEMS_PER_PAGE)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
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
        per_page=ITEMS_PER_PAGE,
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
