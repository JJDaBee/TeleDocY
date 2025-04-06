SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;

CREATE DATABASE IF NOT EXISTS `orderdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `orderdb`;

DROP TABLE IF EXISTS `orders`;

CREATE TABLE IF NOT EXISTS `orders` (
    `orderID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `uuid` CHAR(36) NOT NULL,
    `prescriptions` JSON NOT NULL,
    `prescriptionDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Sample data for order logs --
INSERT INTO `orders` (`uuid`, `prescriptions`, `prescriptionDate`) VALUES
(
    "uuid-1234",
    '[{"medicineName": "Panadol", "quantity": 2, "dosage": "2x daily"}, {"medicineName": "Vitamin C", "quantity": 1, "dosage": "1x daily"}]',
    '2025-03-25 10:00:00'
),
(
    "uuid-5678",
    '[{"medicineName": "Ibuprofen", "quantity": 1, "dosage": "After meals"}, {"medicineName": "Zyrtec", "quantity": 2, "dosage": "Once daily"}]',
    '2025-03-25 11:00:00'
),
(
    "uuid-9101",
    '[{"medicineName": "Amoxicillin", "quantity": 3, "dosage": "3x daily"}]',
    '2025-03-25 12:30:00'
);

COMMIT;
