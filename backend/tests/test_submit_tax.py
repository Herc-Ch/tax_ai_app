import json


def test_submit_and_get(client):
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

    # POST
    res = client.post("/api/submit-tax", json=payload)
    assert res.status_code == 201
    body = res.get_json()
    assert body["message"] == "Received tax info."
    assert body["received"] == payload

    # GET
    res = client.get("/api/submit-tax")
    assert res.status_code == 200
    lst = res.get_json()
    assert isinstance(lst, list) and lst[0] == payload


def test_update_and_delete(client):
    # insert one record
    client.post(
        "/api/submit-tax",
        json={
            "filing_status": "single",
            "age": 25,
            "country": "GR",
            "employment_type": "emp",
            "income": 10000,
            "work_expenses": 0,
            "mortgage_interest": 0,
            "charity_donations": 0,
            "education_expenses": 0,
            "retirement_contributions": 0,
            "dependents": 0,
        },
    )

    # PUT valid
    update = {
        "index": 0,
        "income": 15000,
        "filing_status": "married",
        "age": 26,
        "country": "GR",
        "employment_type": "emp",
        "work_expenses": 0,
        "mortgage_interest": 0,
        "charity_donations": 0,
        "education_expenses": 0,
        "retirement_contributions": 0,
        "dependents": 0,
    }
    res = client.put("/api/submit-tax", json=update)
    assert res.status_code == 200

    # DELETE valid
    res = client.delete("/api/submit-tax?index=0")
    assert res.status_code == 200


def test_invalid_methods(client):
    # missing required fields
    res = client.post("/api/submit-tax", json={"age": 30})
    assert res.status_code == 400
    assert "errors" in res.get_json()
