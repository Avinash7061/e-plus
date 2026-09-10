-- PRAHARI / E+ Database Schema
-- PostgreSQL / Supabase

-- =========================================
-- USERS
-- =========================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    age INTEGER,
    phone TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================
-- HEALTH READINGS
-- =========================================

CREATE TABLE IF NOT EXISTS health_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    heart_rate INTEGER,
    spo2 NUMERIC(5,2),
    body_temperature NUMERIC(5,2),
    activity_level TEXT,

    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================
-- ENVIRONMENTAL READINGS
-- =========================================

CREATE TABLE IF NOT EXISTS environmental_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID
        REFERENCES users(id)
        ON DELETE CASCADE,

    temperature NUMERIC(5,2),
    humidity NUMERIC(5,2),
    air_quality_index NUMERIC(6,2),

    hazard_type TEXT,

    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================
-- RISK ASSESSMENTS
-- =========================================

CREATE TABLE IF NOT EXISTS risk_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    health_reading_id UUID
        REFERENCES health_readings(id)
        ON DELETE SET NULL,

    environmental_reading_id UUID
        REFERENCES environmental_readings(id)
        ON DELETE SET NULL,

    risk_level TEXT NOT NULL
        CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),

    risk_score NUMERIC(5,2),

    reason TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================
-- ALERTS
-- =========================================

CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    risk_assessment_id UUID
        REFERENCES risk_assessments(id)
        ON DELETE SET NULL,

    alert_type TEXT NOT NULL,

    message TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'SENT', 'ACKNOWLEDGED')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- =========================================
-- INDEXES
-- =========================================

CREATE INDEX IF NOT EXISTS idx_health_readings_user_id
ON health_readings(user_id);

CREATE INDEX IF NOT EXISTS idx_health_readings_recorded_at
ON health_readings(recorded_at);

CREATE INDEX IF NOT EXISTS idx_environmental_readings_user_id
ON environmental_readings(user_id);

CREATE INDEX IF NOT EXISTS idx_environmental_readings_recorded_at
ON environmental_readings(recorded_at);

CREATE INDEX IF NOT EXISTS idx_risk_assessments_user_id
ON risk_assessments(user_id);

CREATE INDEX IF NOT EXISTS idx_alerts_user_id
ON alerts(user_id);

CREATE INDEX IF NOT EXISTS idx_alerts_status
ON alerts(status);-- [PASTE THE FULL SQL FROM SECTION 4 OF YOUR ARCHITECTURE DOC HERE]
