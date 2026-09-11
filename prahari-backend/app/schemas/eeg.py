"""Pydantic request/response models for EEG session and prediction endpoints."""

from datetime import datetime
from pydantic import BaseModel


class EEGSessionCreate(BaseModel):
    device_id: str | None = None
    sample_rate_hz: int | None = None


class EEGSessionResponse(BaseModel):
    id: str
    user_id: str
    device_id: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    sample_rate_hz: int | None = None


class EEGPredictRequest(BaseModel):
    # TODO: confirm exact shape with ML teammate — currently assumes a flat list 
    # of raw samples for a single-channel window (e.g. 16 floats). Adjust if his 
    # model expects a different shape (multi-channel, different window size, etc.)
    raw_samples: list[float]
    window_start_ms: int


class EEGPredictResponse(BaseModel):
    predicted_class: str
    confidence: float
    window_start_ms: int


class EEGSessionSummaryResponse(BaseModel):
    session: EEGSessionResponse
    predictions: list[EEGPredictResponse]