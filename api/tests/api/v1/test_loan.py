import pytest

from fastapi.testclient import TestClient

from api.tests.api import app


client = TestClient(app)


@pytest.mark.loan
def test_create_loan(loan_parts):
    invalid_uuid = "invalid"
    response = client.post(f"/api/v1/loans/?book_id={invalid_uuid}&user_id={invalid_uuid}")
    assert response.status_code == 422

    fake_uuid = "292ada19-6b06-44f7-a20e-dc6687668b0e"
    response = client.post(f"/api/v1/loans/?book_id={fake_uuid}&user_id={fake_uuid}")
    assert response.status_code == 404

    book_id, user_id = loan_parts
    response = client.post(f"/api/v1/loans/?book_id={book_id}&user_id={user_id}")
    assert response.status_code == 201
