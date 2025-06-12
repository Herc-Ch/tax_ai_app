def test_ai_tax_advice_success(client):
    payload = {
        "filing_status": "single",
        "age": 40,
        "country": "Greece",
        "employment_type": "employee",
        "income": 30000,
        "work_expenses": 100,
        "mortgage_interest": 0,
        "charity_donations": 0,
        "education_expenses": 0,
        "retirement_contributions": 0, 
        "dependents": 0,
    }
    res = client.post("/api/ai-tax-advice", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["advice"] == "This is fake advice"


def test_ai_tax_advice_validation(client):
    # missing required field -> 400
    res = client.post("/api/ai-tax-advice", json={"age": 50})
    assert res.status_code == 400
    assert "errors" in res.get_json()
