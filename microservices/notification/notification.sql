CREATE DATABASE IF NOT EXISTS `notification` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `notification`;

DROP TABLE IF EXISTS `notifications`;

CREATE TABLE IF NOT EXISTS `notifications` (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Insert sample data
INSERT INTO notifications (email, message)
SELECT 'vannessanga24@gmail.com', 'eat 1 panadol'
WHERE NOT EXISTS (
    SELECT 1 FROM notifications WHERE email='vannessanga24@gmail.com' AND message='eat 1 panadol'
);
