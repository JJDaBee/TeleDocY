--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-03-30 14:27:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 24801)
-- Name: doctor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor (
    "doctorID" uuid NOT NULL,
    gender character varying(10) NOT NULL,
    "dateOfBirth" date NOT NULL,
    email character varying(150) NOT NULL,
    phone character varying(20) NOT NULL,
    credentials character varying(50) NOT NULL,
    "yearsOfExperience" integer NOT NULL,
    "medicalLicenseNumber" character varying(100) NOT NULL,
    "doctorName" character varying(200)
);


ALTER TABLE public.doctor OWNER TO postgres;

--
-- TOC entry 4890 (class 0 OID 24801)
-- Dependencies: 217
-- Data for Name: doctor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor ("doctorID", gender, "dateOfBirth", email, phone, credentials, "yearsOfExperience", "medicalLicenseNumber", "doctorName") FROM stdin;
eaac2ebf-93f8-458d-a244-2f5cf2a5c121	Male	1981-01-16	zjiajun58@gmail.com	+65 9123 1009	MD	13	SG2001009I	Tan Wei Ming
fc23ac28-0dce-4b9d-9a17-e494e0fa1369	Male	1985-09-28	zjiajun58@gmail.com	+65 9123 1005	MD	11	SG2001005E	Lee Kai Sheng
27bd85eb-e815-4c69-941d-042f8d2cc127	Female	1989-12-01	zjiajun58@gmail.com	+65 9123 1010	MBBS	10	SG2001010J	Teo Hui Ying
30c84387-d07f-4136-9fd3-4d54647b2b2e	Male	1979-04-19	zjiajun58@gmail.com	+65 9123 1004	MBBS	17	SG2001004D	Ho Wen Bin
8c120123-1aa4-440c-aab8-3a569700b82f	Female	1988-07-24	zjiajun58@gmail.com	+65 9123 1002	MD	9	SG2001002B	Chua Li Ting
9116b4a6-3791-485a-a80e-a3367aa31255	Female	1986-03-12	zjiajun58@gmail.com	+65 9123 1001	MBBS	10	SG2001001A	Chan Pei Pei
9757e8d5-dd94-465b-8ecb-87ecc394874a	Male	1983-10-20	zjiajun58@gmail.com	+65 9123 1008	MBBS	12	SG2001008H	Ong Jia Hao
bc78b9b5-502f-4eb8-a153-ecd0e1df89d6	Female	1990-02-14	zjiajun58@gmail.com	+65 9123 1006	MBBS	8	SG2001006F	Lim Mei Ling
cc78e751-c74e-4ad6-8124-6b162a0e8b06	Female	1987-06-07	zjiajun58@gmail.com	+65 9123 1007	DO	9	SG2001007G	Ng Xuan Yi
ea8f75b3-48a1-4e72-bcf8-68bd3f4eeeb3	Male	1982-11-05	zjiajun58@gmail.com	+65 9123 1003	MBBS	14	SG2001003C	Goh Zhi Hao
\.


--
-- TOC entry 4742 (class 2606 OID 24807)
-- Name: doctor doctor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_pkey PRIMARY KEY ("doctorID");


--
-- TOC entry 4744 (class 2606 OID 24811)
-- Name: doctor unique_medical_license; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT unique_medical_license UNIQUE ("medicalLicenseNumber");


-- Completed on 2025-03-30 14:27:50

--
-- PostgreSQL database dump complete
--

