import os
import json
import logging
from lxml import etree
from functools import reduce

# Configure logging
logger = logging.getLogger(__name__)

DATA_FOLDER = 'data/'
TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
XML_NS = '{http://www.w3.org/XML/1998/namespace}'

# Load type mappings from JSON file
def _load_type_map():
    """Load TYPE_MAP from JSON configuration file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'type_labels.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Create combined map: org types at root level, places nested
        type_map = data['orgs'].copy()
        type_map['places'] = data['places']
        return type_map
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file {config_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading type map from {config_path}: {e}")
        raise

TYPE_MAP = _load_type_map()

def parse_xml(file_name):
    file_path = os.path.join(os.path.dirname(__file__), DATA_FOLDER, file_name)
    parser = etree.XMLParser(resolve_entities=False)

    try:
        tree = etree.parse(file_path, parser)
        return tree
    except etree.XMLSyntaxError as e:
        logger.error(f"Invalid XML format in {file_path}: {e}")
        raise
    except FileNotFoundError:
        logger.error(f"XML file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error parsing file {file_path}: {e}")
        raise

def parse_idnos(element):
    return list(map(lambda idno: {
            'type': idno.get('type'),
            'value': idno.text
        }, element.findall('.//tei:idno', TEI_NS)))

def parse_address(element):
    return list(map(lambda address: {
        'street': address.find('.//tei:street', TEI_NS).text if address.find('.//tei:street', TEI_NS) is not None else None,
        'postCode': address.find('.//tei:postCode', TEI_NS).text if address.find('.//tei:postCode', TEI_NS) is not None else None,
        'settlement': address.find('.//tei:settlement', TEI_NS).text if address.find('.//tei:settlement', TEI_NS) is not None else None
    }, element.findall('.//tei:address', TEI_NS)))

def parse_location(element):
    location = element.find('.//tei:location', TEI_NS)
    if not location:
        return None
    
    country_el = location.find('.//tei:country', TEI_NS)
    country = country_el.get('key') if country_el is not None else None

    return {
        'country': country,
        'geo': location.find('.//tei:geo', TEI_NS).text if location.find('.//tei:geo', TEI_NS) is not None else None,
        'street': location.find('.//tei:street', TEI_NS).text if location.find('.//tei:street', TEI_NS) is not None else None,
        'postCode': location.find('.//tei:postCode', TEI_NS).text if location.find('.//tei:postCode', TEI_NS) is not None else None,
        'settlement': location.find('.//tei:settlement', TEI_NS).text if location.find('.//tei:settlement', TEI_NS) is not None else None
    }

def parse_orgs():
    tree = parse_xml("orgs.xml")
    root = tree.getroot()

    def extract_org_names(org):
        return list(map(lambda org_name: {
            'name': org_name.text,
            'lang': org_name.get(f'{XML_NS}lang')
        }, org.findall('.//tei:orgName', TEI_NS)))

    orgs = list(map(lambda org: {
        'id': org.get(f'{XML_NS}id'),
        'type': org.get('type'),
        'sameAs': org.get('sameAs', None),
        'org_names': extract_org_names(org),
        'desc': org.get('desc', None),
        'idnos': parse_idnos(org),
        'location': parse_location(org)
    }, root.findall('.//tei:org', TEI_NS)))

    return orgs

def parse_people():
    tree = parse_xml("cited-people.xml")
    root = tree.getroot()

    def extract_pers_names(person):
        names_list = []
        for pers_name in person.findall('.//tei:persName', TEI_NS):
            name_parts = []
            for el in pers_name:
                if etree.QName(el).localname in ['roleName', 'forename', 'surname', 'genName']:
                    name_parts.append({
                        'tag': etree.QName(el).localname,
                        'text': el.text,
                        'type': el.get('type'),
                        'ref': el.get('ref')
                    })
            
            full_name = " ".join(part['text'] for part in name_parts if part['text']).strip()

            names_list.append({
                'name': full_name or (pers_name.text and pers_name.text.strip()),
                'lang': pers_name.get(f'{XML_NS}lang'),
                'parts': name_parts
            })
        return names_list

    people = list(map(lambda person: {
        'id': person.get(f'{XML_NS}id'),
        'sameAs': person.get('sameAs', None),
        'sex': person.find('.//tei:sex', TEI_NS).get('value') if person.find('.//tei:sex', TEI_NS) is not None else None,
        'pers_names': extract_pers_names(person),
        'birth': person.find('.//tei:birth/tei:date', TEI_NS).get('when-iso') if person.find('.//tei:birth/tei:date', TEI_NS) is not None else None,
        'birth_place': person.findtext('.//tei:birth/tei:placeName', namespaces=TEI_NS),
        'death': person.find('.//tei:death/tei:date', TEI_NS).get('when-iso') if person.find('.//tei:death/tei:date', TEI_NS) is not None else None,
        'death_place': person.findtext('.//tei:death/tei:placeName', namespaces=TEI_NS),
        'occupations': [occ.text for occ in person.findall('.//tei:occupation', TEI_NS)],
        'affiliations': [aff.findtext('.//tei:orgName', namespaces=TEI_NS) for aff in person.findall('.//tei:affiliation', TEI_NS)],
        'idnos': parse_idnos(person),
        'note': person.findtext('.//tei:note', namespaces=TEI_NS)
    }, root.findall('.//tei:person', TEI_NS)))

    return people

def parse_places():
    tree = parse_xml("places.xml")
    root = tree.getroot()

    def extract_place_names(place):
        return list(map(lambda place_name: {
            'name': place_name.text,
            'lang': place_name.get(f'{XML_NS}lang')
        }, place.findall('.//tei:placeName', TEI_NS)))

    places = list(map(lambda place: {
        'id': place.get(f'{XML_NS}id'),
        'sameAs': place.get('sameAs', None),
        'type': place.get('type'),
        'place_names': extract_place_names(place),
        'location': parse_location(place),
        'idnos': parse_idnos(place)
    }, root.findall('.//tei:place', TEI_NS)))

    return places

def format_iso_date(iso_date_str):
    """Formats an ISO date string into a human-readable Italian date."""
    if not iso_date_str:
        return "N/D"

    is_bc = iso_date_str.startswith('-')
    if is_bc:
        iso_date_str = iso_date_str[1:]

    mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    
    parts = iso_date_str.split('-')
    formatted_date = iso_date_str # fallback
    try:
        if len(parts) == 3: # YYYY-MM-DD
            year, month, day = map(int, parts)
            formatted_date = f"{day} {mesi[month-1]} {year}"
        elif len(parts) == 2: # YYYY-MM
            year, month = map(int, parts)
            formatted_date = f"{mesi[month-1]} {year}"
        elif len(parts) == 1 and parts[0]: # YYYY
            formatted_date = str(int(parts[0]))
    except (ValueError, IndexError):
        pass # Will fall through to returning original string
    
    if is_bc:
        return f"{formatted_date} a.C."
    
    return formatted_date

def format_year(iso_date_str):
    """Formats an ISO date string into just the year, handling B.C. dates."""
    if not iso_date_str:
        return "?"
    
    is_bc = iso_date_str.startswith('-')
    if is_bc:
        iso_date_str = iso_date_str[1:]

    year_str = iso_date_str.split('-')[0]
    
    try:
        # Convert to int and back to str to remove leading zeros
        year_val = int(year_str)
        year = str(year_val)
    except ValueError:
        year_val = None
        year = year_str # Fallback if not a valid integer

    if is_bc:
        return f"{year} a.C."
    
    if year_val is not None and year_val < 1000:
        return f"{year} d.C."

    return year

def filter_entities_by_search(entities, entity_type, search_query):
    """
    Filter entities by search_query for the given entity_type.
    - orgs: search in org_names[].name
    - people: search in pers_names[].parts[].text
    - places: search in place_names[].name
    """
    if not search_query:
        return entities
    sq = search_query.strip().lower()
    if entity_type == 'orgs':
        return [org for org in entities if any(sq in (name['name'] or '').lower() for name in org.get('org_names', []))]
    elif entity_type == 'places':
        return [p for p in entities if any(sq in (name['name'] or '').lower() for name in p.get('place_names', []))]
    elif entity_type == 'people':
        return [person for person in entities if any(sq in (part['text'] or '').lower() for name in person.get('pers_names', []) for part in name.get('parts', []))]
    return entities

def get_news_data():
    """Load and return news data from news.json file, sorted by date descending."""
    file_path = os.path.join(os.path.dirname(__file__), DATA_FOLDER, 'news.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            news = json.load(f)
            # Sort by date descending (most recent first)
            return sorted(news, key=lambda x: x.get('date', ''), reverse=True)
    except FileNotFoundError:
        logger.warning(f"News data file not found: {file_path}. Returning empty list.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in news data file {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading news data from {file_path}: {e}")
        return []

def get_pagination_window(page, total_pages, window=7):
    """Generate pagination window with ellipsis for large page counts."""
    if total_pages <= window:
        return list(range(1, total_pages + 1))
    half = window // 2
    if page <= half + 1:
        return list(range(1, window)) + [None, total_pages]
    elif page >= total_pages - half:
        return [1, None] + list(range(total_pages - window + 2, total_pages + 1))
    else:
        return [1, None] + list(range(page - half + 1, page + half)) + [None, total_pages]
