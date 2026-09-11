import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.core.supabase_client import get_supabase
from app.dependencies import get_current_user

mock_supabase = MagicMock()

def override_get_supabase():
    return mock_supabase

app.dependency_overrides[get_supabase] = override_get_supabase

client = TestClient(app)

def test_unauthenticated_request():
    """Tests that a request without a valid token is rejected with 401"""
    if get_current_user in app.dependency_overrides:
        del app.dependency_overrides[get_current_user]
        
    response = client.post(
        "/ingestion/biometrics",
        headers={"Authorization": "Bearer invalid_token"},
        json={"readings": []}
    )
    assert response.status_code == 401

def test_successful_batch_insert():
    """Tests successful batch insert with 2+ readings"""
    app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-id"}
    
    # Mock the database insert response
    mock_supabase.table().insert().execute.return_value.data = [
        {"id": 1},
        {"id": 2}
    ]
    
    payload = {
        "readings": [
            {"heart_rate": 72, "spo2": 98.5, "recorded_at": "2023-01-01T12:00:00Z"},
            {"heart_rate": 75, "skin_temp": 36.6, "recorded_at": "2023-01-01T12:05:00Z"}
        ]
    }
    
    response = client.post("/ingestion/biometrics", json=payload)
    assert response.status_code == 200
    assert response.json()["inserted_count"] == 2
    assert response.json()["reading_ids"] == [1, 2]

def test_empty_batch():
    """Tests that an empty batch is rejected with 400"""
    app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-id"}
    
    response = client.post("/ingestion/biometrics", json={"readings": []})
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty batch"
