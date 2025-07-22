"""
Configuration for entity types, their parsers, display titles, and type label mappings.
- ENTITY_CONFIG: Maps entity types to their parser and display title.
- ORG_TYPE_MAP: Maps organization type keys to Italian labels.
- PLACE_TYPE_MAP: Maps place type keys to Italian labels.
- TYPE_MAP: Combined map for compatibility (orgs + places).
"""
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

# Organization type labels (for orgs)
ORG_TYPE_MAP = {
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
    'cappella': 'Cappella', 'orfanotrofio': 'Orfanotrofio', 'altro': 'Altro'
}

# Place type labels (for places)
PLACE_TYPE_MAP = {
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

# Combined type map for compatibility (orgs + places)
TYPE_MAP = ORG_TYPE_MAP.copy()
TYPE_MAP['places'] = PLACE_TYPE_MAP 