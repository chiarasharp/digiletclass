from flask import Blueprint, render_template, request, abort
from datetime import datetime
from app.config.entities import ENTITY_CONFIG, TYPE_MAP
from app.utils import get_pagination_window, get_entity_modal_context, filter_entities_by_search, filter_and_paginate_entities, load_json

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    """Render the home page."""
    recent_news = load_json('news.json') or []
    try:
        recent_news.sort(key=lambda e: e.get('date', ''), reverse=True)
    except Exception:
        pass
    recent_news = recent_news[:3]
    return render_template("home.html", recent_news=recent_news)

@main_bp.route("/about/")
def about():
    """Render the about page."""
    return render_template("about.html")



@main_bp.route('/entities')
def entities():
    """Render the entities landing page."""
    return render_template('entities.html')

@main_bp.route('/entities/<string:entity_type>')
def entities_list(entity_type):
    """Render a paginated, filtered list of entities of the given type."""
    if entity_type not in ENTITY_CONFIG:
        abort(404)
    config = ENTITY_CONFIG[entity_type]
    all_data = config['parser']()
    context = filter_and_paginate_entities(entity_type, all_data, request.args, TYPE_MAP)
    return render_template(
        'entities_list.html',
        items=context['paginated_items'],
        item_type=entity_type,
        title=config['title'],
        org_types=context['org_types'],
        place_types=context['place_types'],
        selected_type=context['selected_type'],
        type_map=context['type_map_for_template'],
        page=context['page'],
        per_page=context['per_page'],
        total=context['total'],
        pagination_window=context['pagination_window']
    )

@main_bp.route('/modal/<entity_type>/<entity_id>')
def modal(entity_type, entity_id):
    """Render the modal for a specific entity by type and ID."""
    result = get_entity_modal_context(entity_type, entity_id, TYPE_MAP)
    if not result:
        return '', 404
    template_name, context = result
    return render_template(template_name, **context)

@main_bp.route('/methodology')
def methodology():
    """Render the methodology page."""
    return render_template('methodology.html')

@main_bp.route('/project')
def project():
    """Render the project page."""
    return render_template('project.html')

@main_bp.route('/news')
def news():
    """Render the news and events page."""
    entries = load_json('news.json') or []
    # Sort by date desc
    try:
        entries.sort(key=lambda e: e.get('date', ''), reverse=True)
    except Exception:
        pass
    return render_template('news.html', entries=entries)

@main_bp.route('/news/<string:news_id>')
def news_detail(news_id):
    """Render a single news/event detail page."""
    entries = load_json('news.json') or []
    entry = next((e for e in entries if e.get('id') == news_id), None)
    if not entry:
        abort(404)
    return render_template('news_detail.html', item=entry)
