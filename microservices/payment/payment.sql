CREATE DATABASE IF NOT EXISTS payment;
USE payment;

CREATE TABLE IF NOT EXISTS payment (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample dummy payment record
INSERT INTO payment (paymentID, amount, datetime)
VALUES (1, 10.00, NOW());
