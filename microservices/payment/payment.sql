DROP DATABASE IF EXISTS paymentdb;
CREATE DATABASE IF NOT EXISTS paymentdb;

USE paymentdb;

CREATE TABLE IF NOT EXISTS payments (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL,
    medicine_inventory_list JSON NOT NULL,
    prescription JSON NOT NULL,
    amount FLOAT NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
