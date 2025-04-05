SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;

CREATE DATABASE IF NOT EXISTS `consultationHistory` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `consultationHistory`;

DROP TABLE IF EXISTS `consultationHistory`;

CREATE TABLE IF NOT EXISTS `consultationHistory` (
    `uuid` VARCHAR(20) NOT NULL,
    `nric` VARCHAR(9) NOT NULL,
    `dateTime` DATETIME NOT NULL,
    `reasonForVisit` VARCHAR(1000) NOT NULL,
    `doctorName` VARCHAR(100) NOT NULL,
    `diagnosis` VARCHAR(1000) NOT NULL,
    `prescriptions` VARCHAR(1000) DEFAULT NULL,
    PRIMARY KEY (`uuid`, `dateTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Sample data for consultation history --
INSERT INTO `consultationHistory` (`uuid`, `nric`, `dateTime`, `reasonForVisit`, `doctorName`, `diagnosis`, `prescriptions`) VALUES
("uuid-5678", "S7654321B", "2025-03-01 10:30:00", "Fever and cough", "Teo Hui Ying", "Flu", "Paracetamol 500mg, Cough Syrup"),
("uuid-91011", "T0987654C", "2025-03-10 14:00:00", "Headache", "Teo Hui Ying", "Migraine", "Ibuprofen 200mg"),
("uuid-1234", "T0123456A", "2025-03-15 09:15:00", "Stomach pain", "Goh Zhi Hao", "Gastritis", "Antacid tablets"),
("uuid-9300", "T0987654C", "2025-03-20 16:45:00", "Routine check-up", "Goh Zhi Hao", "Normal", "Multivitamins");

COMMIT;
