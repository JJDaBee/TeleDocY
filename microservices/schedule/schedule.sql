--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-03-30 14:25:12

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
-- TOC entry 217 (class 1259 OID 16576)
-- Name: schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schedule (
    doctorname character varying(100) NOT NULL,
    next_available_time timestamp without time zone
);


ALTER TABLE public.schedule OWNER TO postgres;

--
-- TOC entry 4888 (class 0 OID 16576)
-- Dependencies: 217
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.schedule (doctorname, next_available_time) FROM stdin;
Chua Li Ting	2025-03-30 04:55:43.271995
Ng Xuan Yi	2025-03-30 04:29:28.69404
Ong Jia Hao	2025-03-30 04:38:10.005317
Teo Hui Ying	2025-03-30 04:38:15.167714
Lee Kai Sheng	2025-03-30 04:38:29.225917
Tan Wei Ming	2025-03-30 04:38:30.968836
Chan Pei Pei	2025-03-30 04:38:39.857866
Goh Zhi Hao	2025-03-30 04:38:44.324787
Ho Wen Bin	2025-03-30 04:38:54.803121
Lim Mei Ling	2025-03-30 04:42:23.161507
\.


--
-- TOC entry 4742 (class 2606 OID 16580)
-- Name: schedule doctor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT doctor_pkey PRIMARY KEY (doctorname);


-- Completed on 2025-03-30 14:25:13

--
-- PostgreSQL database dump complete
--

