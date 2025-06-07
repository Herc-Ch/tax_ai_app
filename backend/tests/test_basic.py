def test_health_check(client):
    # Simple check for /api/submit-tax GET to verify server is running
    response = client.get("/api/submit-tax")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


# def test_advice_route(client, mocker):
#     mock_response = {"advice": "Dummy"}
#     mock_openai = mocker.patch(
#         "openai.ChatCompletion.create", return_value=mock_response
#     )
#     response = client.post("/api/advice", json={"data": "test"})
#     assert response.status_code == 200
#     assert "advice" in response.json
