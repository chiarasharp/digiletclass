"""
letters.py
Fetches letter metadata from the public EVT2 digital edition (esdcarteggiocannetifiacchi.unibo.it)
to link entities (people, places, orgs) to the letters in which they are cited.

Data is fetched over HTTP on first use and cached in memory for the lifetime of the process.
No letter data is stored on disk in this repository.
"""
import re
import logging
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from lxml import etree

logger = logging.getLogger(__name__)

EVT_BASE_URL = 'https://esdcarteggiocannetifiacchi.unibo.it/data'
EVT_INDEX_URL = f'{EVT_BASE_URL}/carteggio-canneti-fiacchi.xml'
TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
REF_RE = re.compile(r'#(DLCL_CF_(?:PC|L|O)\d+)')
XML_PARSER = etree.XMLParser(resolve_entities=False, no_network=True, recover=True)

_cache = None  # dict: entity_id -> list of {id, title, date, url}


def _fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={'User-Agent': 'DigiLetClass/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _letter_file_list():
    try:
        data = _fetch(EVT_INDEX_URL)
    except (urllib.error.URLError, TimeoutError) as e:
        logger.warning(f"Could not fetch EVT letters index: {e}")
        return []
    hrefs = re.findall(r'xi:include href="(busta-\d+/[^"]+\.xml)"', data.decode('utf-8'))
    return hrefs


def _parse_letter(href):
    url = f'{EVT_BASE_URL}/{href}'
    try:
        data = _fetch(url)
    except (urllib.error.URLError, TimeoutError) as e:
        logger.warning(f"Could not fetch letter {href}: {e}")
        return None

    root = etree.fromstring(data, parser=XML_PARSER)
    letter_id = root.get('{http://www.w3.org/XML/1998/namespace}id')
    title_el = root.find('.//tei:titleStmt/tei:title', TEI_NS)
    title = title_el.text.strip() if title_el is not None and title_el.text else letter_id
    if '...luogo' in title or '...anno' in title:
        title = re.sub(r'\s*\([^)]*\)\s*$', '', title).strip()
    date_el = root.find('.//tei:correspAction[@type="sent"]/tei:date', TEI_NS)
    date = (date_el.get('when-iso') or None) if date_el is not None else None

    # First <pb> id is used as the EVT "page" deep-link target; later <pb> ids in the
    # source data are sometimes malformed (duplicated busta prefix), so only the first is trusted.
    first_pb = root.find('.//tei:pb', TEI_NS)
    first_pb_id = first_pb.get('{http://www.w3.org/XML/1998/namespace}id') if first_pb is not None else None

    entity_ids = set(REF_RE.findall(data.decode('utf-8')))

    return {
        'id': letter_id,
        'title': title,
        'date': date,
        'href': href,
        'first_pb_id': first_pb_id,
        'entity_ids': entity_ids,
    }


def _build_cache():
    hrefs = _letter_file_list()
    if not hrefs:
        return {}

    letters = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = [pool.submit(_parse_letter, href) for href in hrefs]
        for future in as_completed(futures):
            result = future.result()
            if result:
                letters.append(result)

    by_entity = {}
    for letter in letters:
        for entity_id in letter['entity_ids']:
            by_entity.setdefault(entity_id, []).append({
                'id': letter['id'],
                'title': letter['title'],
                'date': letter['date'],
                'href': letter['href'],
                'first_pb_id': letter['first_pb_id'],
            })

    for entity_id in by_entity:
        by_entity[entity_id].sort(key=lambda l: (l['date'] is None, l['date'] or ''))

    return by_entity


def get_letters_for_entity(entity_id):
    """Returns a list of letters citing the given entity ID, or [] if none/unavailable."""
    global _cache
    if _cache is None:
        _cache = _build_cache()
    return _cache.get(entity_id, [])


def letter_evt_url(letter_id, first_pb_id=None):
    url = f'https://esdcarteggiocannetifiacchi.unibo.it/#/imgTxt?d={letter_id}'
    if first_pb_id:
        url += f'&p={first_pb_id}'
    return url
