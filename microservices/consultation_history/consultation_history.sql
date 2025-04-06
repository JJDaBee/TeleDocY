SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;

CREATE DATABASE IF NOT EXISTS `consultationHistory` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `consultationHistory`;

DROP TABLE IF EXISTS `consultationHistory`;

CREATE TABLE IF NOT EXISTS `consultationHistory` (
    `uuid` VARCHAR(20) NOT NULL,
    `dateTime` DATETIME NOT NULL,
    `reasonForVisit` VARCHAR(1000) NOT NULL,
    `doctorName` VARCHAR(100) NOT NULL,
    `diagnosis` VARCHAR(1000) NOT NULL,
    `prescriptions` JSON DEFAULT NULL,
    PRIMARY KEY (`uuid`, `dateTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Sample data for consultation history --
INSERT INTO `consultationHistory` (`uuid`, `dateTime`, `reasonForVisit`, `doctorName`, `diagnosis`, `prescriptions`) VALUES
("uuid-5678", "2025-03-01 10:30:00", "Fever and cough", "Ng Xuan Yi", "Flu", '[{"medicineName": "Panadol", "quantity": 2, "dosage": "2x daily"}, {"medicineName": "Vitamin C", "quantity": 1, "dosage": "1x daily"}]'),
("uuid-91011", "2025-03-10 14:00:00", "Headache", "Ng Xuan Yi", "Migraine", '[{"medicineName": "Ibuprofen", "quantity": 1, "dosage": "After meals"}, {"medicineName": "Zyrtec", "quantity": 2, "dosage": "Once daily"}]'),
("uuid-1234", "2025-03-15 09:15:00", "Stomach pain", "Ong Jia Hao", "Gastritis", '[{"medicineName": "Amoxicillin", "quantity": 3, "dosage": "3x daily"}]'),
("uuid-9300", "2025-03-20 16:45:00", "Routine check-up", "Ong Jia Hao", "Normal", '[{"medicineName": "Zyrtec", "quantity": 2, "dosage": "Once daily"}]');

COMMIT;
