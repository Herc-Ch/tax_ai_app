def test_submit_tax_realistic(client):
    payload = {
        "filing_status": "single",
        "age": 30,
        "country": "Greece",
        "employment_type": "employee",
        "income": 40000,
        "work_expenses": 500,
        "mortgage_interest": 3000,
        "charity_donations": 200,
        "education_expenses": 1000,
        "retirement_contributions": 800,
        "dependents": 1,
    }
    res = client.post("/api/submit-tax", json=payload)
    assert res.status_code == 201
    assert "Received tax info." in res.get_json()["message"]
    assert res.get_json()["received"] == payload


def test_submit_tax_get(client):
    res = client.get("/api/submit-tax")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
