import os
from lxml import etree
from functools import reduce

DATA_FOLDER = 'data/'
TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
XML_NS = '{http://www.w3.org/XML/1998/namespace}'

def parse_xml(file_name):
    print("Current working directory:", os.getcwd())
    
    file_path = os.path.join(os.path.dirname(__file__), DATA_FOLDER, file_name)
    
    print(f"Attempting to open XML file: {file_path}")  # Debugging output
    
    parser = etree.XMLParser(resolve_entities=False)

    try:
        tree = etree.parse(file_path, parser)
        return tree
    except etree.XMLSyntaxError as e:
        print(f"Invalid XML format in {file_path}: {e}")
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")

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
    return {
        'country': location.find('.//tei:country', TEI_NS).get('key', None),
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
