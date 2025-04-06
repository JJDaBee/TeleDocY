\c doctor;

BEGIN;
-- Create the doctor table
DROP TABLE IF EXISTS public.doctor;

CREATE TABLE IF NOT EXISTS public.doctor (
    doctorid UUID NOT NULL,
    gender VARCHAR(10) NOT NULL,
    dateofbirth DATE NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    yearsofexperience INTEGER NOT NULL,
    medicallicensenumber VARCHAR(100) NOT NULL,
    doctorname VARCHAR(200) NOT NULL,
    picture TEXT,
    PRIMARY KEY (doctorName),
    CONSTRAINT unique_medical_license UNIQUE (medicalLicenseNumber)
);

-- Insert sample data
INSERT INTO public.doctor (
    doctorid, gender, dateofbirth, email, phone, yearsofexperience,
    medicallicensenumber, doctorname, picture
) VALUES
('27bd85eb-e815-4c69-941d-042f8d2cc127', 'Female', '1989-12-01', 'zjiajun58@gmail.com', '+65 9123 1010', 10, 'SG2001010J', 'Teo Hui Ying', 'doctor_pics/Teo_Hui_Ying.jpg'),
('9757e8d5-dd94-465b-8ecb-87ecc394874a', 'Male', '1983-10-20', 'zjiajun58@gmail.com', '+65 9123 1008', 12, 'SG2001008H', 'Ong Jia Hao', 'doctor_pics/Ong_Jia_Hao.jpg'),
('cc78e751-c74e-4ad6-8124-6b162a0e8b06', 'Female', '1987-06-07', 'zjiajun58@gmail.com', '+65 9123 1007', 9, 'SG2001007G', 'Ng Xuan Yi', 'doctor_pics/Ng_Xuan_Yi.webp'),
('eaac2ebf-93f8-458d-a244-2f5cf2a5c121', 'Male', '1981-01-16', 'zjiajun58@gmail.com', '+65 9123 1009', 13, 'SG2001009I', 'Tan Wei Ming', 'doctor_pics/Tan_Wei_Ming.avif'),
('fc23ac28-0dce-4b9d-9a17-e494e0fa1369', 'Male', '1985-09-28', 'zjiajun58@gmail.com', '+65 9123 1005', 11, 'SG2001005E', 'Lee Kai Sheng', 'doctor_pics/Lee_Kai_Sheng.jpg');

COMMIT;