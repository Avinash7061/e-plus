# E+ 🛡️

**AI-powered, privacy-preserving personal health companion for disaster-health resilience**

Built for **Smart India Hackathon 2025** — Problem Statement **SIH26181**

---

## 📌 Overview

PRAHARI monitors biometric and environmental signals in real time to protect vulnerable populations — rural communities, the elderly, and outdoor workers — during disaster-health events like heat waves, floods, and pollution spikes.

The project also includes an advanced **Phase 2 module**: an in-ear EEG earbud capable of predicting seizure onset, repositioned from the team's original research focus into the broader disaster-resilience pitch.

---

## 🧠 Model Functioning (EEG Seizure Classification)

This is the core ML component of the Phase 2 module, and the part of the project with the most technical depth.

### Problem
Classify EEG signal windows into one of four states:
1. Healthy
2. Generalized Seizure
3. Focal Seizure
4. Seizure Event

### Dataset
- **Source:** BEED (Bonn EEG Epilepsy Dataset)-style data, ~8,000 labeled samples
- Each sample is a short window of raw EEG signal (16 samples per window) with a class label

### Feature Engineering — the key design decision
A pure feature-engineering approach (discarding raw values) underperformed, because 16-sample windows are too short for engineered features alone to retain enough signal. The model instead uses a **hybrid feature vector**:

| Feature group | What it captures |
|---|---|
| Raw signal values | The unprocessed waveform itself, preserved as direct input |
| Statistical features | Mean, variance, skewness, kurtosis of the window |
| Hjorth parameters | Activity, mobility, complexity — standard EEG descriptors of signal dynamics |
| FFT band power | Frequency-domain energy across relevant EEG bands (e.g. delta, theta, alpha, beta) |

Concatenating raw values with these engineered features gave a large accuracy jump over engineered-features-only — this was the single biggest lever in model performance.

### Model
- **Algorithm:** Random Forest Classifier (`scikit-learn`)
- **Artifact:** `eeg_best_model.joblib`
- **Accuracy:** ~94–95% on held-out data across all 4 classes

> ⚠️ **Note:** Local development environment does not have `xgboost` installed, so any XGBoost-based experiments silently fall back to `GradientBoostingClassifier`. Random Forest remains the primary/best-performing model.

### Inference
```python
import joblib
import numpy as np

model = joblib.load("eeg_best_model.joblib")

# feature_vector = [raw_values..., statistical_features..., hjorth_params..., fft_band_powers...]
prediction = model.predict([feature_vector])
probabilities = model.predict_proba([feature_vector])
```

### Known limitations (for judges / reviewers)
- Single-channel EEG has inherent limits compared to clinical multi-channel montages — positioned as a **wellness screening aid**, not a diagnostic device, to stay within a defensible scope.
- Published seizure-prediction lead times vary widely (~10–45 minutes) depending on method and patient cohort; PRAHARI cites a range rather than a fixed number.
- Not clinically validated — intentionally scoped this way for hackathon-stage feasibility.

---

## 🏗️ System Architecture

### Core MVP — Disaster-Health Resilience
- **Data sources:** Phone sensors, Google Health Connect API, IMD Weather API, CPCB/OpenAQ air quality data
- **On-device inference:** TensorFlow Lite
- **Backend:** FastAPI + PostgreSQL/Supabase
- **Alerts:** Twilio (SMS) + Firebase Cloud Messaging (push)
- **Frontend:** React / Next.js dashboard

### Phase 2 — EEG Earbud Hardware
| Component | Part | Purpose |
|---|---|---|
| Analog front-end | TI **ADS1292R** | EEG signal acquisition + built-in electrode impedance detection |
| Motion sensing | BMI270 IMU | Cancels motion artifacts from raw EEG |
| Compute/BLE | nRF5340 (dual-core) | On-device processing + Bluetooth streaming |
| Audio | Knowles balanced armature driver | Earbud audio output |

> The **ADS1292R** (not the base ADS1292) is used specifically for its built-in impedance monitoring — an important distinction for technical reviewers evaluating signal-quality claims.

---

## 🔐 Privacy & Compliance
- Designed to comply with **DPDP Act 2023** for biosignal and personal health data.
- EEG device positioned as a **wellness device**, not a medical/diagnostic device, avoiding clinical-validation and regulatory blockers at this stage.

---

## 🛠️ Tech Stack
- **ML:** scikit-learn, joblib, NumPy
- **Backend:** FastAPI, PostgreSQL / Supabase
- **Frontend:** React, Next.js
- **On-device ML:** TensorFlow Lite
- **Hardware:** TI ADS1292R, BMI270, nRF5340, Knowles balanced armature driver
- **APIs:** Google Health Connect, IMD Weather API, CPCB/OpenAQ, Twilio, FCM

---

## 📂 Project Structure
```
PRAHARI/
├── model/
│   ├── eeg_best_model.joblib
│   ├── train_model.py
│   ├── feature_engineering.py
│   └── model_detail.md
├── backend/
│   └── (FastAPI app, Supabase integration)
├── frontend/
│   └── (React/Next.js dashboard)
├── hardware/
│   └── (schematics, firmware notes)
├── docs/
│   └── PRAHARI - SIH26181 Idea Presentation.pptx
└── README.md
```

---

## 🚦 Status
Actively developed for SIH 2025. Core disaster-health MVP is the primary submission; EEG earbud module is presented as a Phase 2 roadmap item.

---

## 👥 Team
_Add team name/ID here_

---

## 📄 License
_Add license here (e.g. MIT)_
