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
  deliveryAddress VARCHAR(1000) PRIMARY KEY NOT NULL,
  medication VARCHAR(1000) NOT NULL,
  deliverySurcharge INT NOT NULL,
  deliveryDate datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO deliveryDetail (deliveryAddress, medication, deliverySurcharge, deliveryDate) VALUES
('123 Bedok North Avenue 3, #05-01, Singapore 460123', 'Paracetamol 500mg, Vitamin C 1000mg', 3, '2024-04-01 10:30:00'),
('25 Jurong West Street 42, #12-04, Singapore 640025', 'Ibuprofen 200mg', 5, '2024-04-02 14:00:00'),
('9 Tampines Central 1, #03-11, Singapore 529536', 'Cetirizine 10mg, Loratadine 10mg', 2, '2024-04-03 09:00:00'),
('888 Woodlands Drive 50, #11-18, Singapore 730888', 'Metformin 850mg', 4, '2024-04-04 17:30:00'),
('301 Clementi Avenue 2, #06-09, Singapore 129901', 'Omeprazole 20mg, Antacid Tablets', 3, '2024-04-05 11:15:00');

COMMIT;