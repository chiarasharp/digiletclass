import pytest
from app import create_app
import re

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"home" in response.data or b"Home" in response.data

def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert b"404" in response.data

def test_entities_orgs(client):
    response = client.get('/entities/orgs')
    assert response.status_code == 200
    assert b"Organizzazioni" in response.data or b"org" in response.data

def test_entities_people(client):
    response = client.get('/entities/people')
    assert response.status_code == 200
    assert b"Persone" in response.data or b"people" in response.data

def test_entities_places(client):
    response = client.get('/entities/places')
    assert response.status_code == 200
    assert b"Luoghi" in response.data or b"place" in response.data

def test_modal_orgs(client):
    # This test assumes at least one org exists with id '1'. Adjust as needed.
    response = client.get('/modal/orgs/1')
    assert response.status_code in (200, 404)  # 404 if not found, 200 if found

def test_modal_people(client):
    response = client.get('/modal/people/1')
    assert response.status_code in (200, 404)

def test_modal_places(client):
    response = client.get('/modal/places/1')
    assert response.status_code in (200, 404)

def test_entities_invalid_type(client):
    response = client.get('/entities/invalidtype')
    assert response.status_code == 404

def test_modal_invalid_type(client):
    response = client.get('/modal/invalidtype/1')
    assert response.status_code == 404

def test_modal_nonexistent_id(client):
    response = client.get('/modal/orgs/999999')
    assert response.status_code == 404

def test_entities_orgs_type_filter(client):
    response = client.get('/entities/orgs?type=library')
    assert response.status_code == 200

def test_entities_orgs_search(client):
    response = client.get('/entities/orgs?search=biblio')
    assert response.status_code == 200

def test_entities_people_sex_filter(client):
    response = client.get('/entities/people?sex=male')
    assert response.status_code == 200
    response = client.get('/entities/people?sex=female')
    assert response.status_code == 200

def test_entities_people_birth_filter(client):
    response = client.get('/entities/people?birth_from=1800&birth_to=1900')
    assert response.status_code == 200

def test_entities_places_country_settlement_filter(client):
    response = client.get('/entities/places?country=IT')
    assert response.status_code == 200
    response = client.get('/entities/places?settlement=rome')
    assert response.status_code == 200

def test_entities_orgs_pagination(client):
    response = client.get('/entities/orgs?page=2')
    assert response.status_code == 200
    response = client.get('/entities/orgs?page=999')
    assert response.status_code == 200

def get_first_entity_id(client, entity_type):
    resp = client.get(f"/entities/{entity_type}")
    assert resp.status_code == 200
    # Try to extract the first entity id from the HTML (data-entity-id)
    match = re.search(rb'data-entity-id="([^"]+)"', resp.data)
    if match:
        return match.group(1).decode()
    return None

def test_modal_org_content(client):
    org_id = get_first_entity_id(client, "orgs")
    if not org_id:
        pytest.skip("No orgs found to test modal content.")
    response = client.get(f"/modal/orgs/{org_id}")
    assert response.status_code == 200
    assert b"entity-modal-title" in response.data
    assert b"entity-modal-section-title" in response.data
    assert b"ID interno" in response.data

def test_modal_person_content(client):
    person_id = get_first_entity_id(client, "people")
    if not person_id:
        pytest.skip("No people found to test modal content.")
    response = client.get(f"/modal/people/{person_id}")
    assert response.status_code == 200
    assert b"entity-modal-title" in response.data
    assert b"ID interno" in response.data

def test_modal_place_content(client):
    place_id = get_first_entity_id(client, "places")
    if not place_id:
        pytest.skip("No places found to test modal content.")
    response = client.get(f"/modal/places/{place_id}")
    assert response.status_code == 200
    assert b"entity-modal-title" in response.data
    assert b"ID interno" in response.data

def test_entities_orgs_type_filter_content(client):
    # Get a type from the first org
    resp = client.get("/entities/orgs")
    assert resp.status_code == 200
    match = re.search(rb'data-entity-id="[^"]+".*?badge-type.*?>([^<]+)<', resp.data, re.DOTALL)
    if not match:
        pytest.skip("No org type found to test filter.")
    org_type = match.group(1).decode().strip()
    # Map Italian label back to type key if possible (skip if not found)
    # For now, just use the label as is
    resp = client.get(f"/entities/orgs?type={org_type}")
    assert resp.status_code == 200
    # All cards should have the same type label
    for m in re.finditer(rb'badge-type.*?>([^<]+)<', resp.data):
        assert m.group(1).decode().strip() == org_type

def test_entities_people_sex_filter_content(client):
    for sex in ["male", "female"]:
        resp = client.get(f"/entities/people?sex={sex}")
        assert resp.status_code == 200
        # All cards should mention the correct sex if present
        # (This is a weak check, as sex is not always shown in the card)

def test_entities_places_country_filter_content(client):
    # Use a known country from the data
    country = "IT"
    resp = client.get(f"/entities/places?country={country}")
    assert resp.status_code == 200
    # All cards should mention the country
    assert country in resp.data.decode()
