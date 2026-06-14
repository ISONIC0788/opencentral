-- =============================================
-- Central Database Schema + Utilities
-- =============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- =============================================
-- TABLES
-- =============================================

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS organisations (
    id BIGSERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    members JSONB NOT NULL DEFAULT '[]'::jsonb,
    max_rooms INTEGER NOT NULL DEFAULT 5,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rooms (
    room TEXT PRIMARY KEY,
    room_type TEXT NOT NULL DEFAULT 'standard',
    max_log_size BIGINT NOT NULL DEFAULT 104857600,
    owner_type TEXT NOT NULL CHECK (owner_type IN ('user', 'org')),
    owner_id TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'private' CHECK (visibility IN ('private', 'public')),
    shared_with JSONB NOT NULL DEFAULT '[]'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Main logs table
CREATE TABLE IF NOT EXISTS logs (
    id BIGSERIAL PRIMARY KEY,
    room TEXT NOT NULL REFERENCES rooms(room) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    username TEXT NOT NULL REFERENCES users(username) ON DELETE SET NULL,
    avatar_url TEXT,
    level TEXT NOT NULL,
    module TEXT NOT NULL,
    message TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '3 days'),
    size_bytes INTEGER NOT NULL DEFAULT 0
);

-- =============================================
-- INDEXES
-- =============================================

CREATE INDEX idx_rooms_owner ON rooms (owner_type, owner_id);
CREATE INDEX idx_rooms_updated_at ON rooms (updated_at);
CREATE INDEX idx_rooms_visibility ON rooms (visibility);

CREATE INDEX idx_logs_room_time ON logs (room, "timestamp" DESC);
CREATE INDEX idx_logs_room_id ON logs (room, id DESC);
CREATE INDEX idx_logs_room_level ON logs (room, level);
CREATE INDEX idx_logs_room_user ON logs (room, "username");
CREATE INDEX idx_logs_room_module ON logs (room, module);
CREATE INDEX idx_logs_message_trgm ON logs USING GIN (message gin_trgm_ops);  -- fast text search

-- =============================================
-- TRIGGER: Update room timestamp
-- =============================================

CREATE OR REPLACE FUNCTION update_room_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE rooms SET updated_at = NOW() WHERE room = NEW.room;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_room_ts
AFTER INSERT ON logs
FOR EACH ROW EXECUTE FUNCTION update_room_timestamp();

-- =============================================
-- RETENTION CLEANUP (Time-based per room type)
-- =============================================

CREATE OR REPLACE FUNCTION cleanup_expired_logs()
RETURNS void AS $$
BEGIN
    DELETE FROM logs 
    WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- VIEWS
-- =============================================

CREATE OR REPLACE VIEW room_log_stats AS
SELECT 
    r.room,
    r.room_type,
    r.max_log_size,
    pg_size_pretty(r.max_log_size) as max_size_pretty,
    COALESCE(SUM(l.size_bytes), 0) as current_size_bytes,
    pg_size_pretty(COALESCE(SUM(l.size_bytes), 0)) as current_size_pretty,
    COUNT(l.id) as log_count,
    (COALESCE(SUM(l.size_bytes), 0)::float / NULLIF(r.max_log_size, 0) * 100)::numeric(5,2) as usage_percent
FROM rooms r
LEFT JOIN logs l ON l.room = r.room
GROUP BY r.room, r.room_type, r.max_log_size
ORDER BY usage_percent DESC;

-- =============================================
-- CRON JOBS
-- =============================================

SELECT cron.schedule('daily-retention',     '0 3 * * *', 'SELECT cleanup_expired_logs();');
SELECT cron.schedule('daily-retention-cleanup', '30 3 * * *', $$
    DELETE FROM users WHERE updated_at < NOW() - INTERVAL '7 days';
$$);

SELECT cron.schedule('cleanup-cron-logs', '0 4 * * *', 
    $$DELETE FROM cron.job_run_details WHERE end_time < NOW() - INTERVAL '1 days';$$
);

ANALYZE users, organisations, rooms, logs;
