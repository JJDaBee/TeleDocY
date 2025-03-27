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
  `uuid` int NOT NULL AUTO_INCREMENT,
  `nric` varchar(9) NOT NULL,
  `dateTime` datetime NOT NULL,
  `reasonForVisit` varchar(1000) NOT NULL,
  `doctorName` varchar(100) NOT NULL,
  `diagnosis` varchar(1000) NOT NULL,
  `prescriptions` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`uuid`,`dateTime`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultationHistory`
--

LOCK TABLES `consultationHistory` WRITE;
/*!40000 ALTER TABLE `consultationHistory` DISABLE KEYS */;
INSERT INTO `consultationHistory` VALUES (1,'S1234567A','2024-03-15 09:30:00','Fever and sore throat','Dr. Tan Wei','Viral Pharyngitis','Paracetamol, Lozenges'),(2,'T2345678B','2024-03-16 14:15:00','Headache and dizziness','Dr. Lim Yong','Migraine','Ibuprofen, Sumatriptan'),(3,'G3456789C','2024-03-17 10:45:00','Persistent cough','Dr. Chua Mei','Bronchitis','Cough syrup, Amoxicillin'),(4,'S4567890D','2024-03-18 11:30:00','Abdominal pain','Dr. Kumar Raj','Gastritis','Omeprazole, Antacid'),(5,'T5678901E','2024-03-19 16:00:00','Skin rash and itching','Dr. Ong Li','Allergic Dermatitis','Antihistamines, Hydrocortisone cream'),(6,'S1111111Z','2024-03-27 15:00:00','Back pain','Dr. Lee','Muscle strain','Ibuprofen'),(7,'S7777777G','2024-04-01 09:45:00','Frequent migraines and blurry vision','Dr. Alicia Tan','Chronic Migraine with Aura','Sumatriptan, Magnesium supplements'),(8,'S7777777G','2024-04-01 09:45:00','Frequent migraines and blurry vision','Dr. Alicia Tan','Chronic Migraine with Aura','Sumatriptan, Magnesium supplements'),(10,'S7777777G','2024-04-01 09:45:00','Frequent migraines and blurry vision','Dr. Alicia Tan','Chronic Migraine with Aura','Sumatriptan, Magnesium supplements');
/*!40000 ALTER TABLE `consultationHistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-27 17:14:05
