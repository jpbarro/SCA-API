from fastapi.testclient import TestClient
from unittest.mock import patch

def test_create_mission_success(client: TestClient):
    mission_data = {
        "targets": [
            {"name": "Dr. Evil", "country": "USA"},
            {"name": "Goldfinger", "country": "Switzerland"}
        ]
    }
    response = client.post("/missions/", json=mission_data)
    assert response.status_code == 201
    data = response.json()
    assert data["complete"] is False
    assert len(data["targets"]) == 2
    assert data["targets"][0]["name"] == "Dr. Evil"

def test_create_mission_fails_with_too_many_targets(client: TestClient):
    mission_data = {
        "targets": [
            {"name": "Target 1", "country": "A"},
            {"name": "Target 2", "country": "B"},
            {"name": "Target 3", "country": "C"},
            {"name": "Target 4", "country": "D"}
        ]
    }
    response = client.post("/missions/", json=mission_data)
    assert response.status_code == 422

def test_assign_cat_to_mission(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True):
        cat_res = client.post("/cats/", json={"name": "Agent 00-Cat", "years_of_experience": 7, "breed": "Siamese", "salary": 150000.0})
    cat_id = cat_res.json()["id"]

    mission_res = client.post("/missions/", json={"targets": [{"name": "Le Chiffre", "country": "Montenegro"}]})
    mission_id = mission_res.json()["id"]

    assign_res = client.patch(f"/missions/{mission_id}/assign?cat_id={cat_id}")
    assert assign_res.status_code == 200
    data = assign_res.json()
    assert data["cat_id"] == cat_id
    
    cat_data = client.get(f"/cats/{cat_id}").json()
    assert cat_data["mission"]["id"] == mission_id

def test_delete_unassigned_mission(client: TestClient):
    mission_res = client.post("/missions/", json={"targets": [{"name": "Scaramanga", "country": "Thailand"}]})
    mission_id = mission_res.json()["id"]
    
    delete_res = client.delete(f"/missions/{mission_id}")
    assert delete_res.status_code == 204

    get_res = client.get(f"/missions/{mission_id}")
    assert get_res.status_code == 404

def test_cannot_delete_assigned_mission(client: TestClient):
    with patch('app.services.validate_cat_breed', return_value=True):
        cat_res = client.post("/cats/", json={"name": "Pussy Galore", "years_of_experience": 6, "breed": "Russian Blue", "salary": 130000.0})
    cat_id = cat_res.json()["id"]
    mission_res = client.post("/missions/", json={"targets": [{"name": "Oddjob", "country": "USA"}]})
    mission_id = mission_res.json()["id"]
    client.patch(f"/missions/{mission_id}/assign?cat_id={cat_id}")

    delete_res = client.delete(f"/missions/{mission_id}")
    assert delete_res.status_code == 400
    assert delete_res.json()["detail"] == "Cannot delete a mission that is assigned to a cat"

def test_update_target_notes_and_completion(client: TestClient):
    mission_res = client.post("/missions/", json={"targets": [{"name": "Mr. White", "country": "Italy"}, {"name": "Vesper Lynd", "country": "Italy"}]})
    mission_data = mission_res.json()
    target_id_1 = mission_data["targets"][0]["id"]
    target_id_2 = mission_data["targets"][1]["id"]
    mission_id = mission_data["id"]

    update_res = client.patch(f"/targets/{target_id_1}", json={"notes": "He has a white cat."})
    assert update_res.status_code == 200
    assert update_res.json()["notes"] == "He has a white cat."
    assert update_res.json()["complete"] is False

    client.patch(f"/targets/{target_id_1}", json={"complete": True})
    
    mission_check = client.get(f"/missions/{mission_id}").json()
    assert mission_check["complete"] is False

    client.patch(f"/targets/{target_id_2}", json={"complete": True})

    mission_check_2 = client.get(f"/missions/{mission_id}").json()
    assert mission_check_2["complete"] is True

    final_update_res = client.patch(f"/targets/{target_id_1}", json={"notes": "This should fail."})
    assert final_update_res.status_code == 400
    assert "mission is already complete" in final_update_res.json()["detail"]