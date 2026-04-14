from fastapi.testclient import TestClient


def test_expenses_exist_for_auth_user(auth_client: TestClient):
    assert auth_client.get("/expenses").status_code == 200


def test_unauth_user_gets_401(annonymus_client: TestClient):
    assert annonymus_client.get("/expenses").status_code == 401
    assert annonymus_client.get("/expenses/1").status_code == 401
    assert annonymus_client.delete("/expenses/1").status_code == 401


def test_get_non_existing_expense_404(auth_client: TestClient):
    get_response = auth_client.get("/expenses/1000000")
    assert get_response.status_code == 404
    assert "not found" in get_response.json().get("message")


def test_delete_non_existing_expense_404(auth_client: TestClient):
    assert auth_client.delete("/expenses/1000000").status_code == 404


def test_get_existing_expense_200(auth_client: TestClient):
    assert auth_client.get("/expenses/1").status_code == 200


def test_create_and_delete_expense(auth_client: TestClient):

    # Check getting 201 response as creating a new expense
    expense = {"amount": 1041, "description": "test"}
    post_response = auth_client.post("/expenses", json=expense)
    assert post_response.status_code == 201

    # Check getting 200 response as getting created expense
    # and check equality of values
    get_response = auth_client.get("/expenses/11")
    assert get_response.status_code == 200
    assert get_response.json().get("amount") == 1041
    assert get_response.json().get("description") == "test"

    # Check getting 204 response as deleting an expense
    delete_response = auth_client.delete("/expenses/11")
    assert delete_response.status_code == 204

    # Check getting 404 response as getting deleted expense
    get_response = auth_client.get("/expenses/11")
    assert get_response.status_code == 404
    assert get_response.json().get("error")


def test_update_expense(auth_client: TestClient):
    expense = {"amount": 500, "description": "test"}
    put_response = auth_client.put("/expenses/1", json=expense)
    assert put_response.status_code == 201

    get_response = auth_client.get("/expenses/1")
    assert get_response.status_code == 200
    assert get_response.json().get("amount") == 500
    assert get_response.json().get("description") == "test"
