-- =========================================
-- Schedule Table Initialization
-- For PostgreSQL (Docker-ready)
-- =========================================

-- Optional: Uncomment if not using POSTGRES_DB=schedule
-- CREATE DATABASE schedule;
-- \connect schedule;

BEGIN;

-- Drop the table if it exists (useful for dev)
DROP TABLE IF EXISTS public.schedule;

-- Create the schedule table
CREATE TABLE public.schedule (
    doctorname VARCHAR(100) PRIMARY KEY,
    next_available_time TIMESTAMP,
    roomid VARCHAR(50) 
);

-- Insert seed data
INSERT INTO public.schedule (doctorname, next_available_time, roomid) VALUES
('Ng Xuan Yi', '2025-03-30 04:29:28.69404', 'bbb49a24-c51a-4266-8dcc-91d1d3428245'),
('Ong Jia Hao', '2025-03-30 04:38:10.005317', 'bbbc9263-e1bf-4c36-90ee-fc17ed2328d6'),
('Teo Hui Ying', '2025-03-30 04:38:15.167714', 'bbbcccf8-2372-4a12-94bc-537b2f521e14'),
('Lee Kai Sheng', '2025-03-30 04:38:29.225917', 'bbbcc9c7-468b-424d-854f-0b6116d2646a'),
('Tan Wei Ming', '2025-03-30 04:38:30.968836', 'bbb78e5a-44e5-4788-acc6-7b7786344b08');

COMMIT;
