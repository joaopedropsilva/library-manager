from fastapi.testclient import TestClient

from api.tests.integration.api import app


client = TestClient(app)


def test_case():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello from library-manager"}
