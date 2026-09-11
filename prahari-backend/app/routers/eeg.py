"""EEG session management and seizure prediction endpoints (Phase 2)."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from app.dependencies import get_current_user
from app.core.supabase_client import get_supabase
from app.schemas.eeg import (
    EEGSessionCreate,
    EEGSessionResponse,
    EEGPredictRequest,
    EEGPredictResponse,
    EEGSessionSummaryResponse,
)
from app.services.eeg_inference import predict as run_eeg_prediction

router = APIRouter(prefix="/eeg", tags=["eeg"])


@router.post("/sessions", response_model=EEGSessionResponse)
def start_session(
    request: EEGSessionCreate,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_supabase),
):
    """Starts a new EEG recording session for the current user."""
    result = (
        db.table("eeg_sessions")
        .insert(
            {
                "user_id": current_user["id"],
                "device_id": request.device_id,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "sample_rate_hz": request.sample_rate_hz,
            }
        )
        .execute()
    )
    return result.data[0]


@router.post("/sessions/{session_id}/predict", response_model=EEGPredictResponse)
def predict_window(
    session_id: str,
    request: EEGPredictRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_supabase),
):
    """Runs a prediction on one window of raw EEG samples and stores the result."""
    session = db.table("eeg_sessions").select("*").eq("id", session_id).execute()
    if not session.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    try:
        result = run_eeg_prediction(request.raw_samples)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    db.table("eeg_predictions").insert(
        {
            "session_id": session_id,
            "predicted_class": result["predicted_class"],
            "confidence": result["confidence"],
            "window_start_ms": request.window_start_ms,
        }
    ).execute()

    return EEGPredictResponse(
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
        window_start_ms=request.window_start_ms,
    )


@router.get("/sessions/{session_id}", response_model=EEGSessionSummaryResponse)
def get_session_summary(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_supabase),
):
    """Returns session details plus all predictions made during it."""
    session = db.table("eeg_sessions").select("*").eq("id", session_id).execute()
    if not session.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    predictions = (
        db.table("eeg_predictions")
        .select("*")
        .eq("session_id", session_id)
        .order("predicted_at", desc=False)
        .execute()
    )

    return EEGSessionSummaryResponse(
        session=session.data[0],
        predictions=predictions.data or [],
    )