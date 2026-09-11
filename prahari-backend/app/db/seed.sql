-- Demo seed data -- run after schema.sql / migrations, for local dev and demo only.

INSERT INTO users (id, full_name, phone_number, email, region) VALUES
    ('11111111-1111-1111-1111-111111111111', 'Test User One', '+919990000001', 'user1@example.com', 'Jaipur'),
    ('22222222-2222-2222-2222-222222222222', 'Test User Two', '+919990000002', 'user2@example.com', 'Jodhpur')
ON CONFLICT (id) DO NOTHING;

INSERT INTO devices (id, user_id, device_type, device_name) VALUES
    ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 'phone', 'Demo Phone A'),
    ('44444444-4444-4444-4444-444444444444', '22222222-2222-2222-2222-222222222222', 'wearable', 'Demo Band B')
ON CONFLICT (id) DO NOTHING;

INSERT INTO health_readings (user_id, device_id, metric_type, value, unit, recorded_at) VALUES
    ('11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 'heart_rate', 78, 'bpm', now() - interval '1 hour'),
    ('11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 'heart_rate', 145, 'bpm', now() - interval '10 minutes'),
    ('22222222-2222-2222-2222-222222222222', '44444444-4444-4444-4444-444444444444', 'spo2', 96, '%', now() - interval '30 minutes');

INSERT INTO environmental_readings (region, hazard_type, value, unit, source, recorded_at) VALUES
    ('Jaipur', 'heat_index', 42.5, 'celsius', 'IMD', now() - interval '1 hour'),
    ('Jodhpur', 'aqi', 210, 'aqi', 'CPCB', now() - interval '1 hour');

INSERT INTO consent_logs (user_id, data_category, purpose) VALUES
    ('11111111-1111-1111-1111-111111111111', 'biometric', 'hazard_alerting'),
    ('22222222-2222-2222-2222-222222222222', 'biometric', 'hazard_alerting');
