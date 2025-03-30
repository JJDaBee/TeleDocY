SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- 
-- Database: medicineInventory
-- 
CREATE DATABASE IF NOT EXISTS medicineInventory DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE medicineInventory;

-- --------------------------------------------------------

--
-- Table structure for table medicineInventory
--

DROP TABLE IF EXISTS medicineInventory;
CREATE TABLE IF NOT EXISTS medicineInventory (
  medicationName VARCHAR(255) PRIMARY KEY NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  quantityLeft INT DEFAULT 0,
  nextRestockDate DATETIME DEFAULT NULL,
  allergies VARCHAR(1000) DEFAULT 'None'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table medicineInventory
--

INSERT INTO medicineInventory (medicationName, price, quantityLeft, nextRestockDate, allergies) VALUES
('Paracetamol', '5.00', 50, '2025-03-10', 'None'),
('Ibuprofen', '8.50', 30, '2025-03-15', 'None'),
('Cetirizine', '6.00', 20, '2025-03-20', 'None'),
('Amoxicillin', '12.00', 15, '2025-03-18', 'Penicillin'),
('Loratadine', '7.50', 25, '2025-03-22', 'None'),
('Metformin', '15.00', 40, '2025-04-01', 'None'),
('Aspirin', '4.00', 60, '2025-03-12', 'None'),
('Cough Syrup', '10.00', 12, '2025-03-25', 'None'),
('Vitamin C', '9.50', 80, '2025-04-05', 'None'),
('Insulin', '25.00', 5, '2025-03-30', 'None'),
('Omeprazole', '11.00', 18, '2025-03-28', 'None'),
('Hydroxyzine', '8.00', 10, '2025-04-03', 'None');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;