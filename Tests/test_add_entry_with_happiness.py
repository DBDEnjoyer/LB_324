import pytest
from app import app, entries  # assumes your Flask app file is named app.py


@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Clear entries before each test so order/index 0 is predictable
    entries.clear()
    with app.test_client() as c:
        yield c


def test_add_entry_with_happiness(client):
    # POST without logging in; the route must still accept it
    resp = client.post(
        "/add_entry",
        data={"content": "Test Entry Content", "happiness": "😃"},
        follow_redirects=False,
    )

    # The spec expects a 302 redirect to "/"
    assert resp.status_code == 302
    # Some servers return absolute URLs; endswith("/") is robust
    assert resp.headers["Location"].endswith("/")

    # The newest entry must be at index 0
    entry = entries[0]
    assert entry is not None
    assert entry.content == "Test Entry Content"
    assert entry.happiness == "😃"
