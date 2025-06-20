from fastapi.testclient import TestClient
from unittest.mock import patch

def test_create_spy_cat_success(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True) as mock_validate:
        response = client.post(
            "/cats/",
            json={"name": "Shadow", "years_of_experience": 4, "breed": "Bombay", "salary": 90000.0}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Shadow"
        assert data["breed"] == "Bombay"
        assert "id" in data
        mock_validate.assert_called_once_with("Bombay")

def test_create_spy_cat_invalid_breed(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=False) as mock_validate:
        response = client.post(
            "/cats/",
            json={"name": "Fluffy", "years_of_experience": 1, "breed": "InvalidBreed", "salary": 50000.0}
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Breed 'InvalidBreed' is not a valid cat breed."}
        mock_validate.assert_called_once_with("InvalidBreed")

def test_read_spy_cats(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True):
        client.post(
            "/cats/",
            json={"name": "Garfield", "years_of_experience": 10, "breed": "Persian", "salary": 120000.0}
        )

    response = client.get("/cats/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Garfield"

def test_read_single_cat(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True):
        create_response = client.post(
            "/cats/",
            json={"name": "Tom", "years_of_experience": 2, "breed": "Domestic Shorthair", "salary": 60000.0}
        )
    cat_id = create_response.json()["id"]

    response = client.get(f"/cats/{cat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Tom"
    assert data["id"] == cat_id

def test_read_nonexistent_cat(client: TestClient):
    response = client.get("/cats/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cat not found"}

def test_update_cat_salary(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True):
        create_response = client.post(
            "/cats/",
            json={"name": "Sylvester", "years_of_experience": 8, "breed": "Tuxedo", "salary": 95000.0}
        )
    cat_id = create_response.json()["id"]

    update_response = client.patch(
        f"/cats/{cat_id}",
        json={"salary": 100000.0}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["salary"] == 100000.0
    assert data["name"] == "Sylvester"

def test_delete_cat(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True):
        create_response = client.post(
            "/cats/",
            json={"name": "Felix", "years_of_experience": 5, "breed": "Bombay", "salary": 80000.0}
        )
    cat_id = create_response.json()["id"]

    delete_response = client.delete(f"/cats/{cat_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/cats/{cat_id}")
    assert get_response.status_code == 404