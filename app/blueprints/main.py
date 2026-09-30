from flask import Blueprint, render_template, request, abort, send_from_directory, current_app
import os
from datetime import datetime
from app.utils import get_news_data, TYPE_MAP, get_pagination_window, parse_orgs, parse_people, parse_places, filter_entities_by_search
from app.letters import get_letters_for_entity, letter_evt_url

main_bp = Blueprint('main', __name__)

# Constants
ITEMS_PER_PAGE = 12
LETTERS_PER_PAGE = 10
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

@main_bp.route('/entities')
def entities():
    from app.utils import parse_people, parse_places, parse_orgs
    counts = {
        'people': len(parse_people()),
        'places': len(parse_places()),
        'orgs': len(parse_orgs()),
    }
    return render_template('entities.html', counts=counts)

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
            filtered_data = [org for org in filtered_data if org.get('location') and org['location'].get('country') and country in org['location'].get('country', '').upper()]
        if settlement:
            filtered_data = [org for org in filtered_data if org.get('location') and org['location'].get('settlement') and settlement in org['location'].get('settlement', '').lower()]
    elif entity_type == 'places':
        place_types = sorted(list(set(p.get('type', 'none') for p in all_data)))
        if selected_type != 'all':
            filtered_data = [p for p in all_data if p.get('type', 'none') == selected_type]
        filtered_data = filter_entities_by_search(filtered_data, 'places', search_query)
        country = request.args.get('country', '').strip().upper()
        settlement = request.args.get('settlement', '').strip().lower()
        if country:
            filtered_data = [p for p in filtered_data if p.get('location') and p['location'].get('country') and country in p['location'].get('country', '').upper()]
        if settlement:
            filtered_data = [p for p in filtered_data if p.get('location') and p['location'].get('settlement') and settlement in p['location'].get('settlement', '').lower()]
    elif entity_type == 'people':
        filtered_data = filter_entities_by_search(filtered_data, 'people', search_query)
        sex = request.args.get('sex', '').strip().lower()
        occupation = request.args.get('occupation', '').strip().lower()
        birth_from = request.args.get('birth_from', '').strip()
        birth_to = request.args.get('birth_to', '').strip()
        if sex:
            filtered_data = [person for person in filtered_data if person.get('sex', '').lower() == sex]
        if occupation:
            filtered_data = [person for person in filtered_data if any(occupation in occ.lower() for occ in (person.get('occupations') or []))]

        def birth_year(person):
            birth = person.get('birth')
            if not birth:
                return None
            is_bc = birth.startswith('-')
            year_part = birth[1:5] if is_bc else birth[:4]
            if not year_part.isdigit():
                return None
            year = int(year_part)
            return -year if is_bc else year

        if birth_from:
            try:
                birth_from_year = int(birth_from)
                filtered_data = [person for person in filtered_data if birth_year(person) is not None and birth_year(person) >= birth_from_year]
            except ValueError:
                pass
        if birth_to:
            try:
                birth_to_year = int(birth_to)
                filtered_data = [person for person in filtered_data if birth_year(person) is not None and birth_year(person) <= birth_to_year]
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
    map_items = []
    if entity_type == 'places':
        map_items = [p for p in filtered_data if p.get('location') and p['location'].get('geo')]
    return render_template(
        'entities_list.html',
        items=paginated_items,
        map_items=map_items,
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

def _paginated_letters(entity_id):
    all_letters = get_letters_for_entity(entity_id)
    page = request.args.get('letters_page', 1, type=int)
    total = len(all_letters)
    total_pages = max(1, int((total + LETTERS_PER_PAGE - 1) / LETTERS_PER_PAGE))
    page = max(1, min(page, total_pages))
    start = (page - 1) * LETTERS_PER_PAGE
    return {
        'entries': all_letters[start:start + LETTERS_PER_PAGE],
        'total': total,
        'page': page,
        'total_pages': total_pages,
        'pagination_window': get_pagination_window(page, total_pages),
    }

@main_bp.route('/orgs/<string:entity_id>')
def org_detail(entity_id):
    data = parse_orgs()
    item = next((o for o in data if o['id'] == entity_id), None)
    if not item:
        abort(404)
    name = item['org_names'][0]['name'] if item.get('org_names') and item['org_names'][0].get('name') else item['id']
    letters = _paginated_letters(entity_id)
    return render_template('entity_detail.html', item_type='orgs', entity_id=entity_id, title=name, org=item, type_map=TYPE_MAP, letters=letters, letter_evt_url=letter_evt_url)

@main_bp.route('/people/<string:entity_id>')
def person_detail(entity_id):
    data = parse_people()
    item = next((p for p in data if p['id'] == entity_id), None)
    if not item:
        abort(404)
    name_parts = item['pers_names'][0]['parts'] if item.get('pers_names') else []
    name = ' '.join(p['text'] for p in name_parts if p.get('text') and p.get('type') not in ['nickname', 'pseudonym', 'translation']).strip()
    name = name or item['id']
    letters = _paginated_letters(entity_id)
    return render_template('entity_detail.html', item_type='people', entity_id=entity_id, title=name, person=item, letters=letters, letter_evt_url=letter_evt_url)

@main_bp.route('/places/<string:entity_id>')
def place_detail(entity_id):
    data = parse_places()
    item = next((p for p in data if p['id'] == entity_id), None)
    if not item:
        abort(404)
    name = item['place_names'][0]['name'] if item.get('place_names') and item['place_names'][0].get('name') else item['id']
    letters = _paginated_letters(entity_id)
    return render_template('entity_detail.html', item_type='places', entity_id=entity_id, title=name, place=item, type_map=TYPE_MAP.get('places', {}), letters=letters, letter_evt_url=letter_evt_url)

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

@main_bp.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

@main_bp.route('/api/openapi.yaml')
def openapi_spec():
    static_dir = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_dir, 'openapi.yaml', mimetype='application/yaml')

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
