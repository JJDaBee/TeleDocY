SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;

CREATE DATABASE IF NOT EXISTS 'consultationHistory' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_c1;
USE 'consultationHistory';

DROP TABLE IF EXISTS 'consultationHistory';
CREATE TABLE IF NOT EXISTS 'consultationHistory' (
    'patientId' int NOT NULL AUTO_INCREMENT,
    'NRIC' VARCHAR(9) NOT NULL,
    'dateTime' DATETIME NOT NULL,
    'reasonForVisit' VARCHAR(1000) NOT NULL,
    'doctorName' VARCHAR(100) NOT NULL,
    'diagnosis' VARCHAR(1000) NOT NULL,
    'prescriptions' VARCHAR(1000),
    PRIMARY KEY ('patientId', 'dateTime')
);

-- sample data for table 'consultation history' -- 

INSERT INTO `consultationHistory` (`patientId`, `NRIC`, `dateTime`, `reasonForVisit`, `doctorName`, `diagnosis`, `prescriptions`) 
VALUES
(1, 'S1234567A', '2024-03-15 09:30:00', 'Fever and sore throat', 'Dr. Tan Wei', 'Viral Pharyngitis', 'Paracetamol, Lozenges'),
(2, 'T2345678B', '2024-03-16 14:15:00', 'Headache and dizziness', 'Dr. Lim Yong', 'Migraine', 'Ibuprofen, Sumatriptan'),
(3, 'G3456789C', '2024-03-17 10:45:00', 'Persistent cough', 'Dr. Chua Mei', 'Bronchitis', 'Cough syrup, Amoxicillin'),
(4, 'S4567890D', '2024-03-18 11:30:00', 'Abdominal pain', 'Dr. Kumar Raj', 'Gastritis', 'Omeprazole, Antacid'),
(5, 'T5678901E', '2024-03-19 16:00:00', 'Skin rash and itching', 'Dr. Ong Li', 'Allergic Dermatitis', 'Antihistamines, Hydrocortisone cream');

