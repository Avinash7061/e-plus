-- E+/PRAHARI database schema
-- Run this against your Supabase Postgres instance (SQL Editor or psql).

CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- needed for gen_random_uuid()

-- Users of the app (patients / monitored individuals)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    date_of_birth DATE,
    region TEXT,                       -- matches environmental_readings.region for lookup
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Devices/phones registered per user (Health Connect source, wearables, EEG earbud, etc.)
CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_type TEXT NOT NULL,         -- 'phone', 'wearable', 'eeg_earbud'
    device_name TEXT,
    registered_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Raw biometric readings ingested from Health Connect / sensors
CREATE TABLE IF NOT EXISTS health_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id) ON DELETE SET NULL,
    metric_type TEXT NOT NULL CHECK (metric_type IN (
        'heart_rate', 'spo2', 'body_temp', 'steps', 'skin_temp', 'respiration_rate'
    )),
    value NUMERIC NOT NULL,
    unit TEXT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_health_readings_user_time
    ON health_readings (user_id, recorded_at DESC);

-- Environmental hazard data pulled from IMD / CPCB / OpenAQ
CREATE TABLE IF NOT EXISTS environmental_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region TEXT NOT NULL,
    hazard_type TEXT NOT NULL CHECK (hazard_type IN (
        'heat_index', 'aqi', 'flood_risk', 'humidity'
    )),
    value NUMERIC NOT NULL,
    unit TEXT NOT NULL,
    source TEXT NOT NULL,              -- 'IMD', 'CPCB', 'OpenAQ'
    recorded_at TIMESTAMPTZ NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_env_readings_region_time
    ON environmental_readings (region, recorded_at DESC);

-- Alerts fired when a biometric or environmental threshold is crossed
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    hazard_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'moderate', 'high', 'critical')),
    message TEXT NOT NULL,
    delivery_channel TEXT CHECK (delivery_channel IN ('sms', 'push', 'both')),
    delivery_status TEXT NOT NULL DEFAULT 'pending' CHECK (delivery_status IN (
        'pending', 'sent', 'failed', 'acknowledged'
    )),
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_alerts_user_time
    ON alerts (user_id, triggered_at DESC);

-- DPDP Act 2023 consent tracking -- what data, for what purpose, and when
CREATE TABLE IF NOT EXISTS consent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    data_category TEXT NOT NULL,       -- 'biometric', 'location', 'health_history'
    purpose TEXT NOT NULL,             -- 'hazard_alerting', 'model_improvement'
    consented_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    revoked_at TIMESTAMPTZ
);
