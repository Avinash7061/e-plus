"""Router tests for /eeg endpoints — Supabase and model inference are mocked."""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.supabase_client import get_supabase
from app.dependencies import get_current_user

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_supabase, None)


def test_start_session_unauthenticated():
    response = client.post("/eeg/sessions", json={})
    assert response.status_code == 401


def test_start_session_success():
    mock_db = MagicMock()
    mock_db.table().insert().execute.return_value.data = [
        {
            "id": "session-1",
            "user_id": "user-1",
            "device_id": None,
            "started_at": "2026-01-01T00:00:00Z",
            "ended_at": None,
            "sample_rate_hz": 256,
        }
    ]
    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1"}
    app.dependency_overrides[get_supabase] = lambda: mock_db

    response = client.post("/eeg/sessions", json={"sample_rate_hz": 256})
    assert response.status_code == 200
    assert response.json()["id"] == "session-1"


def test_predict_session_not_found():
    mock_db = MagicMock()
    mock_db.table().select().eq().execute.return_value.data = []
    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1"}
    app.dependency_overrides[get_supabase] = lambda: mock_db

    response = client.post(
        "/eeg/sessions/nonexistent/predict",
        json={"raw_samples": [0.1] * 16, "window_start_ms": 0},
    )
    assert response.status_code == 404


@patch("app.routers.eeg.run_eeg_prediction")
def test_predict_success(mock_predict):
    mock_predict.return_value = {"predicted_class": "healthy", "confidence": 0.92}

    mock_db = MagicMock()
    mock_db.table().select().eq().execute.return_value.data = [{"id": "session-1"}]
    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1"}
    app.dependency_overrides[get_supabase] = lambda: mock_db

    response = client.post(
        "/eeg/sessions/session-1/predict",
        json={"raw_samples": [0.1] * 16, "window_start_ms": 500},
    )
    assert response.status_code == 200
    assert response.json()["predicted_class"] == "healthy"
    assert response.json()["confidence"] == 0.92


@patch("app.routers.eeg.run_eeg_prediction")
def test_predict_model_not_found_returns_503(mock_predict):
    mock_predict.side_effect = FileNotFoundError("model missing")

    mock_db = MagicMock()
    mock_db.table().select().eq().execute.return_value.data = [{"id": "session-1"}]
    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1"}
    app.dependency_overrides[get_supabase] = lambda: mock_db

    response = client.post(
        "/eeg/sessions/session-1/predict",
        json={"raw_samples": [0.1] * 16, "window_start_ms": 0},
    )
    assert response.status_code == 503