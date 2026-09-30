from flask import Blueprint, jsonify, request
from app.utils import parse_orgs, parse_places, parse_people, filter_entities_by_search

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

ITEMS_PER_PAGE = 25


def _paginate(items, page, per_page):
    total = len(items)

    if per_page is None:
        return {
            'page': 1,
            'per_page': total,
            'total': total,
            'total_pages': 1,
            'items': items,
        }

    start = (page - 1) * per_page
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': max(1, (total + per_page - 1) // per_page),
        'items': items[start:start + per_page],
    }


def _get_per_page():
    raw = request.args.get('per_page', '').strip().lower()
    if raw == 'all':
        return None
    return ITEMS_PER_PAGE


def _cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@api_bp.after_request
def add_cors(response):
    return _cors(response)


# --- People ---

@api_bp.route('/people')
def people_list():
    data = parse_people()
    data = sorted(data, key=lambda x: x.get('pers_names', [{}])[0].get('name', '') or '')

    search = request.args.get('search', '').strip()
    sex = request.args.get('sex', '').strip().lower()
    birth_from = request.args.get('birth_from', '').strip()
    birth_to = request.args.get('birth_to', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = _get_per_page()

    data = filter_entities_by_search(data, 'people', search)
    if sex:
        data = [p for p in data if (p.get('sex') or '').lower() == sex]
    if birth_from:
        try:
            y = int(birth_from)
            data = [p for p in data if p.get('birth') and p['birth'][:4].isdigit() and int(p['birth'][:4]) >= y]
        except ValueError:
            pass
    if birth_to:
        try:
            y = int(birth_to)
            data = [p for p in data if p.get('birth') and p['birth'][:4].isdigit() and int(p['birth'][:4]) <= y]
        except ValueError:
            pass

    return jsonify(_paginate(data, page, per_page))


@api_bp.route('/people/<string:entity_id>')
def people_detail(entity_id):
    data = parse_people()
    item = next((p for p in data if p['id'] == entity_id), None)
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item)


# --- Places ---

@api_bp.route('/places')
def places_list():
    data = parse_places()
    data = sorted(data, key=lambda x: x.get('place_names', [{}])[0].get('name', '') or '')

    search = request.args.get('search', '').strip()
    place_type = request.args.get('type', '').strip()
    country = request.args.get('country', '').strip().upper()
    page = request.args.get('page', 1, type=int)
    per_page = _get_per_page()

    data = filter_entities_by_search(data, 'places', search)
    if place_type:
        data = [p for p in data if (p.get('type') or '') == place_type]
    if country:
        data = [p for p in data if p.get('location') and (p['location'].get('country') or '').upper() == country]

    return jsonify(_paginate(data, page, per_page))


@api_bp.route('/places/<string:entity_id>')
def places_detail(entity_id):
    data = parse_places()
    item = next((p for p in data if p['id'] == entity_id), None)
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item)


# --- Orgs ---

@api_bp.route('/orgs')
def orgs_list():
    data = parse_orgs()
    data = sorted(data, key=lambda x: x.get('org_names', [{}])[0].get('name', '') or '')

    search = request.args.get('search', '').strip()
    org_type = request.args.get('type', '').strip()
    country = request.args.get('country', '').strip().upper()
    settlement = request.args.get('settlement', '').strip().lower()
    page = request.args.get('page', 1, type=int)
    per_page = _get_per_page()

    data = filter_entities_by_search(data, 'orgs', search)
    if org_type:
        data = [o for o in data if (o.get('type') or 'none') == org_type]
    if country:
        data = [o for o in data if o.get('location') and (o['location'].get('country') or '').upper() == country]
    if settlement:
        data = [o for o in data if o.get('location') and (o['location'].get('settlement') or '').lower() == settlement]

    return jsonify(_paginate(data, page, per_page))


@api_bp.route('/orgs/<string:entity_id>')
def orgs_detail(entity_id):
    data = parse_orgs()
    item = next((o for o in data if o['id'] == entity_id), None)
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item)
