def test_submit_tax_post(client):
    res = client.post("/api/submit-tax", json={"name": "John", "income": 40000})
    assert res.status_code == 201
    assert "Received tax info." in res.get_json()["message"]

def test_submit_tax_get(client):
    res = client.get("/api/submit-tax")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
