from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_calculate_edges():
    # Тест эндпоинта /edges
    response = client.post(
        "/edges",
        json=[
            {
                "fixture_id": 1,
                "team_id": 101,
                "market": "Match Winner",
                "k_dec": 2.0,
                "p_model": 0.6,
                "description": "Team A vs Team B"
            }
        ]
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["edge"] > 0
    assert data[0]["fixture_id"] == 1
    assert data[0]["team_id"] == 101

def test_allocate_bets():
    # Тест эндпоинта /allocate
    response = client.post(
        "/allocate",
        json={
            "bets": [
                {
                    "fixture_id": 1,
                    "team_id": 101,
                    "market": "Match Winner",
                    "k_dec": 2.0,
                    "p_model": 0.6,
                    "edge": 0.2
                }
            ],
            "bank": 1000,
            "fraction_multiplier": 0.5,
            "max_total_risk": 0.1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "bets" in data
    assert len(data["bets"]) == 1
    assert "amount" in data["bets"][0]
    assert data["bets"][0]["amount"] > 0
