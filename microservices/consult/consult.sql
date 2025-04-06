-- Drop and recreate the table
DROP TABLE IF EXISTS consults;

CREATE TABLE IF NOT EXISTS consults (
    firstname VARCHAR(100) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    doctorname VARCHAR(100) NOT NULL,
    roomid VARCHAR(50) NOT NULL,
    symptom TEXT NOT NULL,
    medicalhistory TEXT,
    PRIMARY KEY (firstname, datetime)
    -- FOREIGN KEY (doctorname) REFERENCES schedule(doctorname) -- optional
);

-- Optional insert sample
-- INSERT INTO consults (firstname, datetime, doctorname, roomid, symptom, medicalhistory) VALUES
-- ('Alice', '2025-04-06 10:00:00', 'Teo Hui Ying', 'Room101', 'Fever and cough', 'Allergic to penicillin');
