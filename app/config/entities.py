"""
Configuration for entity types, their parsers, display titles, and type label mappings.
- ENTITY_CONFIG: Maps entity types to their parser and display title.
- ORG_TYPE_MAP: Maps organization type keys to Italian labels (loaded from JSON).
- PLACE_TYPE_MAP: Maps place type keys to Italian labels (loaded from JSON).
- TYPE_MAP: Combined map for compatibility (orgs + places, loaded from JSON).
"""
import os
import json
from app.utils import parse_orgs, parse_people, parse_places

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

# Load type labels from JSON configuration
def _load_type_labels():
    """Load type labels from JSON configuration file."""
    config_path = os.path.join(os.path.dirname(__file__), 'type_labels.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

_type_labels = _load_type_labels()

# Organization type labels (for orgs)
ORG_TYPE_MAP = _type_labels['orgs']

# Place type labels (for places)
PLACE_TYPE_MAP = _type_labels['places']

# Combined type map for compatibility (orgs + places)
TYPE_MAP = ORG_TYPE_MAP.copy()
TYPE_MAP['places'] = PLACE_TYPE_MAP 