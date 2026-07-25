-- ============================================================
--  init.sql — runs automatically when Postgres starts for the
--  first time (mounted into /docker-entrypoint-initdb.d/)
-- ============================================================

-- Create the tasks table if it doesn't already exist.
-- SERIAL = auto-incrementing integer (Postgres equivalent of AUTOINCREMENT).
CREATE TABLE IF NOT EXISTS tasks (
    id    SERIAL  PRIMARY KEY,
    title TEXT    NOT NULL,
    done  BOOLEAN NOT NULL DEFAULT FALSE
);

-- Insert three seed tasks ONLY if the table is empty.
-- This INSERT ... SELECT pattern is safe to run multiple times:
-- if tasks already exist, the WHERE NOT EXISTS blocks the insert.
INSERT INTO tasks (title, done)
SELECT title, done FROM (VALUES
    ('Buy groceries', FALSE),
    ('Walk the dog',  FALSE),
    ('Read a book',   TRUE)
) AS seed(title, done)
WHERE NOT EXISTS (SELECT 1 FROM tasks);
