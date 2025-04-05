SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;

CREATE DATABASE IF NOT EXISTS 'notification' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_c1;
USE 'notification';

DROP TABLE IF EXISTS 'notification';
CREATE TABLE IF NOT EXISTS 'notification' (
    'uuid' VARCHAR(20) NOT NULL PRIMARY KEY,
    'notificationLog' VARCHAR(1000) NOT NULL,
    'dateTime' DATETIME NOT NULL,
    'status' VARCHAR(100) NOT NULL,
);

--sample data for notification logs --
INSERT INTO 'notification' ('uuid', 'nric', 'notificationLog', 'dateTime', 'status') VALUES
("uuid-5678", 'Your appointment is confirmed for 25th March.', '2025-03-22 10:30:00', 'Sent'),
("uuid-91011", 'Your lab results are ready for collection.', '2025-03-22 11:00:00', 'Delivered'),
("uuid-1234", 'Reminder: Follow-up appointment on 1st April.', '2025-03-22 12:00:00', 'Pending'),
("uuid-9300", 'Payment received. Thank you!', '2025-03-22 13:30:00', 'Sent'),

COMMIT;