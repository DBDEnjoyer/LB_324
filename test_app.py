from app import app, entries
import pytest

@pytest.fixture()
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_add_entry_with_happiness(client):
    resp = client.post('/add_entry', data={'content': 'Test Entry Content', 'happiness': '😃'})
    assert resp.status_code == 302
    assert resp.headers['Location'] == '/'
    entry = entries[0]
    assert entry is not None
    assert entry.content == 'Test Entry Content'
    assert entry.happiness == '😃'
