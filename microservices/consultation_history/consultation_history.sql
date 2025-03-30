-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: consultationHistory
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `consultationHistory`
--

DROP TABLE IF EXISTS `consultationHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultationHistory` (
  `uuid` varchar(20) NOT NULL AUTO_INCREMENT,
  `nric` varchar(9) NOT NULL,
  `dateTime` datetime NOT NULL,
  `reasonForVisit` varchar(1000) NOT NULL,
  `doctorName` varchar(100) NOT NULL,
  `diagnosis` varchar(1000) NOT NULL,
  `prescriptions` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`uuid`,`dateTime`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

INSERT INTO consultationHistory (uuid, nric, dateTime, reasonForVisit, doctorName, diagnosis, prescriptions) VALUES
("uuid-5678", "S7654321B", "2025-03-01 10:30:00", "Fever and cough", "Teo Hui Ying", "Flu", "Paracetamol 500mg, Cough Syrup"),
("uuid-91011", "T0987654C", "2025-03-10 14:00:00", "Headache", "Teo Hui Ying", "Migraine", "Ibuprofen 200mg"),
("uuid-1234", "T0123456A", "2025-03-15 09:15:00", "Stomach pain", "Goh Zhi Hao", "Gastritis", "Antacid tablets"),
("uuid-9300", "T0987654C", "2025-03-20 16:45:00", "Routine check-up", "Goh Zhi Hao", "Normal", "Multivitamins");

COMMIT;
