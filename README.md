# E+
AI-powered health resilience platform for disaster-prone and vulnerable populations — real-time biometric + environmental monitoring for heat waves, floods, and pollution events, with an in-ear EEG earbud module for seizure prediction (Phase 2). Built for SIH 2025 (PS: SIH26181).

**Privacy-preserving, AI-powered personal health companion for disaster-health resilience**

PRAHARI monitors biometric and environmental signals in real time to protect vulnerable 
populations — rural communities, the elderly, and outdoor workers — during heat waves, 
floods, and pollution events. Built for Smart India Hackathon 2025 (Problem Statement SIH26181).

## 🎯 What it does
- Continuous biometric + environmental monitoring via phone sensors and wearables
- On-device ML inference for early risk detection (heat stress, air quality exposure)
- Real-time alerts via SMS/push notification for at-risk individuals and caregivers
- Privacy-first architecture, DPDP Act 2023 compliant

## 🧠 Phase 2: EEG Seizure Prediction Module
An in-ear EEG earbud (wellness-grade, not diagnostic) streams brain signals to predict 
seizure onset using a Random Forest classifier trained on the BEED EEG dataset, achieving 
~94-95% accuracy across 4 seizure classes.

## 🏗️ Tech Stack
- **Backend:** FastAPI, PostgreSQL/Supabase
- **Frontend:** React / Next.js
- **ML:** scikit-learn, TensorFlow Lite (on-device inference)
- **Hardware:** TI ADS1292R, BMI270 IMU, nRF5340 BLE SoC, Knowles balanced armature driver
- **Integrations:** Google Health Connect, IMD Weather API, CPCB/OpenAQ, Twilio, FCM

## 📊 Status
Actively developed for SIH 2025.
