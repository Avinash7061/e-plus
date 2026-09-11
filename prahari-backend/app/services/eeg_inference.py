"""Loads the trained EEG model and runs predictions on raw signal windows.

TODO: This file currently contains PLACEHOLDER feature extraction and model 
loading. It must be replaced with the ML teammate's actual feature_extraction.py 
logic and his exact eeg_best_model.joblib before this endpoint can produce real 
predictions. Using placeholder logic here would give confidently-wrong results 
with no error — do not deploy/demo this until the real files are wired in.
"""

import logging
from pathlib import Path

import joblib

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).parent.parent / "ml" / "eeg_best_model.joblib"

# TODO: confirm this exact order with the ML teammate — must match training data's 
# label encoding exactly, or predictions will be labeled wrong even if the 
# underlying classification is correct.
CLASS_LABELS = ["healthy", "generalized_seizure", "focal_seizure", "seizure_event"]

_model = None


def _load_model():
    """Lazily loads the model once and caches it."""
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"EEG model not found at {MODEL_PATH}. "
                "Copy eeg_best_model.joblib into app/ml/ before using this endpoint."
            )
        _model = joblib.load(MODEL_PATH)
        logger.info(f"Loaded EEG model from {MODEL_PATH}")
    return _model


def extract_features(raw_samples: list[float]) -> list[float]:
    """PLACEHOLDER — must be replaced with the ML teammate's real feature 
    extraction (Hjorth parameters, FFT band power, statistical features, 
    concatenated with raw values per the project's documented approach).
    
    Returning raw samples unchanged for now purely so the endpoint is 
    exercisable end-to-end with dummy data — this WILL NOT produce meaningful 
    predictions until replaced."""
    logger.warning(
        "extract_features() is a placeholder — real feature extraction from "
        "the ML teammate has not been wired in yet."
    )
    return raw_samples


def predict(raw_samples: list[float]) -> dict:
    """Runs the full pipeline: extract features, predict class + confidence.
    Returns {"predicted_class": str, "confidence": float}."""
    model = _load_model()
    features = extract_features(raw_samples)

    prediction = model.predict([features])[0]
    class_label = (
        CLASS_LABELS[prediction] if isinstance(prediction, int) else str(prediction)
    )

    confidence = 0.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([features])[0]
        confidence = float(max(probabilities))

    return {"predicted_class": class_label, "confidence": confidence}