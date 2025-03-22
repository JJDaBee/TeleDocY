SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;

CREATE DATABASE IF NOT EXISTS 'notification' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_c1;
USE 'notification';

DROP TABLE IF EXISTS 'notification';
CREATE TABLE IF NOT EXISTS 'notification' (
    'patientId' int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'NRIC' VARCHAR(9) NOT NULL,
    'notificationLog' VARCHAR(1000) NOT NULL,
    'dateTime' DATETIME NOT NULL,
    'status' VARCHAR(100) NOT NULL,
);

--sample data for notification logs --
INSERT INTO 'notification' ('patientId', 'NRIC', 'notificationLog', 'dateTime', 'status') VALUES
(1, 'S1234567A', 'Your appointment is confirmed for 25th March.', '2025-03-22 10:30:00', 'Sent'),
(2, 'T2345678B', 'Your lab results are ready for collection.', '2025-03-22 11:00:00', 'Delivered'),
(3, 'G3456789C', 'Reminder: Follow-up appointment on 1st April.', '2025-03-22 12:00:00', 'Pending'),
(4, 'F4567890D', 'Payment received. Thank you!', '2025-03-22 13:30:00', 'Sent'),
(5, 'M5678901E', 'Please update your medical history.', '2025-03-22 14:45:00', 'Failed');
