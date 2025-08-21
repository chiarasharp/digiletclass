"""
Utility functions for parsing XML data, formatting dates, filtering entities, and supporting Flask views.
- XML parsing helpers
- Entity parsing (orgs, people, places)
- Formatting utilities
- Filtering and pagination helpers
- Modal context construction
"""
import os
import json
from lxml import etree
from functools import reduce

DATA_FOLDER = 'data/'
TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
XML_NS = '{http://www.w3.org/XML/1998/namespace}'

# === XML Parsing Helpers ===
def parse_xml(file_name):
    """
    Parse an XML file from the data folder and return an lxml ElementTree.
    """
    file_path = os.path.join(os.path.dirname(__file__), DATA_FOLDER, file_name)
    parser = etree.XMLParser(resolve_entities=False)
    try:
        tree = etree.parse(file_path, parser)
        return tree
    except etree.XMLSyntaxError as e:
        print(f"Invalid XML format in {file_path}: {e}")
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
    
def load_json(file_name):
    """
    Load a JSON file from the data folder and return its parsed content.
    """
    file_path = os.path.join(os.path.dirname(__file__), DATA_FOLDER, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []

def parse_idnos(element):
    """
    Parse all <idno> elements and return a list of dicts with type and value.
    """
    return list(map(lambda idno: {
            'type': idno.get('type'),
            'value': idno.text
        }, element.findall('.//tei:idno', TEI_NS)))

def parse_address(element):
    """
    Parse all <address> elements and return a list of dicts with street, postCode, and settlement.
    """
    return list(map(lambda address: {
        'street': address.find('.//tei:street', TEI_NS).text if address.find('.//tei:street', TEI_NS) is not None else None,
        'postCode': address.find('.//tei:postCode', TEI_NS).text if address.find('.//tei:postCode', TEI_NS) is not None else None,
        'settlement': address.find('.//tei:settlement', TEI_NS).text if address.find('.//tei:settlement', TEI_NS) is not None else None
    }, element.findall('.//tei:address', TEI_NS)))

def parse_location(element):
    """
    Parse a <location> element and return a dict with country, geo, street, postCode, and settlement.
    """
    location = element.find('.//tei:location', TEI_NS)
    if location is None:
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

# === Entity Parsing ===
def parse_orgs():
    """
    Parse orgs.xml and return a list of organization dicts.
    """
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
    """
    Parse cited-people.xml and return a list of person dicts.
    """
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
    """
    Parse places.xml and return a list of place dicts.
    """
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

# === Formatting Utilities ===
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

# === Filtering and Pagination ===
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

def get_pagination_window(page, total_pages, window=7):
    """Return a list of page numbers for pagination controls, with ellipsis (None) if needed."""
    if total_pages <= window:
        return list(range(1, total_pages + 1))
    half = window // 2
    if page <= half + 1:
        return list(range(1, window)) + [None, total_pages]
    elif page >= total_pages - half:
        return [1, None] + list(range(total_pages - window + 2, total_pages + 1))
    else:
        return [1, None] + list(range(page - half + 1, page + half)) + [None, total_pages]

# === Modal Context Construction ===
def get_entity_modal_context(entity_type, entity_id, type_map):
    """
    Returns (template_name, context_dict) for the given entity_type and entity_id, or None if not found.
    """
    if entity_type == 'orgs':
        data = parse_orgs()
        item = next((o for o in data if o['id'] == entity_id), None)
        if not item:
            return None
        return ('_org_modal.html', {'org': item, 'type_map': type_map})
    elif entity_type == 'people':
        data = parse_people()
        item = next((p for p in data if p['id'] == entity_id), None)
        if not item:
            return None
        return ('_person_modal.html', {'person': item})
    elif entity_type == 'places':
        data = parse_places()
        item = next((p for p in data if p['id'] == entity_id), None)
        if not item:
            return None
        return ('_place_modal.html', {'place': item, 'type_map': type_map.get('places', {})})
    else:
        return None

def extract_types(entities, type_key='type'):
    """Extracts and sorts unique types from a list of entities."""
    return sorted(list(set(e.get(type_key, 'none') for e in entities)))

def filter_and_paginate_entities(entity_type, all_data, request_args, type_map, per_page=12):
    """
    Handles normalization, filtering, sorting, and pagination for entities_list.
    Returns: paginated_items, org_types, place_types, selected_type, pagination_window, total, page, type_map_for_template
    """
    # Normalize 'type' for orgs
    if entity_type == 'orgs':
        for item in all_data:
            if not item.get('type'):
                item['type'] = 'none'
    all_data = sorted(all_data, key=lambda x: x.get('name', '').lower())
    selected_type = request_args.get('type', 'all')
    search_query = request_args.get('search', '')
    filtered_data = all_data
    org_types = []
    place_types = []
    if entity_type == 'orgs':
        org_types = extract_types(all_data)
        if selected_type != 'all':
            filtered_data = [org for org in all_data if org.get('type', 'none') == selected_type]
        filtered_data = filter_entities_by_search(filtered_data, 'orgs', search_query)
        country = request_args.get('country', '').strip().upper()
        settlement = request_args.get('settlement', '').strip().lower()
        if country:
            filtered_data = [org for org in filtered_data if org.get('location') and org['location'].get('country') and org['location']['country'].upper() == country]
        if settlement:
            filtered_data = [org for org in filtered_data if org.get('location') and org['location'].get('settlement') and org['location']['settlement'].lower() == settlement]
    elif entity_type == 'places':
        place_types = extract_types(all_data)
        if selected_type != 'all':
            filtered_data = [p for p in all_data if p.get('type', 'none') == selected_type]
        filtered_data = filter_entities_by_search(filtered_data, 'places', search_query)
        country = request_args.get('country', '').strip().upper()
        settlement = request_args.get('settlement', '').strip().lower()
        if country:
            filtered_data = [p for p in filtered_data if p.get('location') and p['location'].get('country') and p['location']['country'].upper() == country]
        if settlement:
            filtered_data = [p for p in filtered_data if p.get('location') and p['location'].get('settlement') and p['location']['settlement'].lower() == settlement]
    elif entity_type == 'people':
        filtered_data = filter_entities_by_search(filtered_data, 'people', search_query)
        sex = request_args.get('sex', '').strip().lower()
        birth_from = request_args.get('birth_from', '').strip()
        birth_to = request_args.get('birth_to', '').strip()
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
    page = request_args.get('page', 1, type=int)
    total = len(filtered_data)
    total_pages = int((total + per_page - 1) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = filtered_data[start:end]
    pagination_window = get_pagination_window(page, total_pages)
    type_map_for_template = {}
    if entity_type == 'orgs':
        type_map_for_template = type_map
    elif entity_type == 'places':
        type_map_for_template = type_map.get('places', {})
    return {
        'paginated_items': paginated_items,
        'org_types': org_types,
        'place_types': place_types,
        'selected_type': selected_type,
        'pagination_window': pagination_window,
        'total': total,
        'page': page,
        'per_page': per_page,
        'type_map_for_template': type_map_for_template
    }
