SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- 
-- Database: deliveryDetail
-- 
CREATE DATABASE IF NOT EXISTS deliveryDetail DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE deliveryDetail;

DROP TABLE IF EXISTS deliveryDetail;

CREATE TABLE IF NOT EXISTS deliveryDetail (
  deliveryID INT AUTO_INCREMENT PRIMARY KEY,
  deliveryAddress VARCHAR(1000) NOT NULL,
  medication JSON NOT NULL,
  deliveryDate DATETIME NOT NULL,
  uuid VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO deliveryDetail (deliveryAddress, medication, deliveryDate, uuid) VALUES
('Block 4 Marsiling Road, #05-01, Singapore 730004', '[{"medicineName": "Amoxicillin", "quantity": 3, "dosage": "3x daily"}]', '2024-04-01 10:30:00', 'uuid-124'),
('Block 373 Jurong East Street 32, #12-04, Singapore 600373', '[{"medicineName": "Panadol", "quantity": 2, "dosage": "2x daily"}, {"medicineName": "Vitamin C", "quantity": 1, "dosage": "1x daily"}]', '2024-04-02 14:00:00', 'uuid-1234'),
('9 Tampines Central 1, #03-11, Singapore 529543', '[{"medicineName": "Ibuprofen", "quantity": 1, "dosage": "After meals"}, {"medicineName": "Zyrtec", "quantity": 2, "dosage": "Once daily"}]', '2024-04-03 09:00:00', 'uuid-5678'),
('888 Woodlands Drive 50, #11-18, Singapore 730888', '[{"medicineName": "Amoxicillin", "quantity": 3, "dosage": "3x daily"}]', '2024-04-04 17:30:00', 'uuid-91011'),
('Block 9 Teck Whye Lane, #06-09, Singapore 680009', '[{"medicineName": "Panadol", "quantity": 2, "dosage": "2x daily"}, {"medicineName": "Vitamin C", "quantity": 1, "dosage": "1x daily"}]', '2024-04-05 11:15:00', 'uuid-1234');

COMMIT;