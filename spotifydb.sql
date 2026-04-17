--
-- PostgreSQL database dump
--

\restrict NgM4o9bNFb92DnU3IcV5KgkCs7WF85ZWzV8WvhdReJLa3oVmsbaGW9cYUMkAadP

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: dim_artists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_artists (
    artist_key integer NOT NULL,
    artist_id character varying(50),
    artist_name character varying(100),
    genre character varying(50)
);


ALTER TABLE public.dim_artists OWNER TO postgres;

--
-- Name: dim_artists_artist_key_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.dim_artists ALTER COLUMN artist_key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dim_artists_artist_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: dim_tracks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_tracks (
    track_key integer NOT NULL,
    track_id character varying(30),
    track_name character varying(100),
    album_key integer,
    duration_ms integer,
    is_explicit boolean
);


ALTER TABLE public.dim_tracks OWNER TO postgres;

--
-- Name: dim_tracks_track_key_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.dim_tracks ALTER COLUMN track_key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dim_tracks_track_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: dim_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_users (
    user_key integer NOT NULL,
    user_id character varying(50),
    display_name character varying(50),
    country character varying(2),
    product character varying(10)
);


ALTER TABLE public.dim_users OWNER TO postgres;

--
-- Name: dim_users_user_key_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.dim_users ALTER COLUMN user_key ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dim_users_user_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: facts_streams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facts_streams (
    stream_id bigint NOT NULL,
    track_key integer,
    user_key integer,
    artist_key integer,
    played_at timestamp without time zone,
    ms_played integer
);


ALTER TABLE public.facts_streams OWNER TO postgres;

--
-- Name: facts_streams_stream_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.facts_streams ALTER COLUMN stream_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.facts_streams_stream_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: stg_spotify_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stg_spotify_raw (
    raw_id integer NOT NULL,
    endpoint text NOT NULL,
    payload jsonb NOT NULL,
    extracted_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.stg_spotify_raw OWNER TO postgres;

--
-- Name: stg_spotify_raw_raw_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.stg_spotify_raw ALTER COLUMN raw_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.stg_spotify_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: dim_artists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_artists (artist_key, artist_id, artist_name, genre) FROM stdin;
\.


--
-- Data for Name: dim_tracks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_tracks (track_key, track_id, track_name, album_key, duration_ms, is_explicit) FROM stdin;
\.


--
-- Data for Name: dim_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_users (user_key, user_id, display_name, country, product) FROM stdin;
\.


--
-- Data for Name: facts_streams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facts_streams (stream_id, track_key, user_key, artist_key, played_at, ms_played) FROM stdin;
\.


--
-- Data for Name: stg_spotify_raw; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stg_spotify_raw (raw_id, endpoint, payload, extracted_at) FROM stdin;
\.


--
-- Name: dim_artists_artist_key_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dim_artists_artist_key_seq', 1, false);


--
-- Name: dim_tracks_track_key_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dim_tracks_track_key_seq', 1, false);


--
-- Name: dim_users_user_key_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dim_users_user_key_seq', 1, false);


--
-- Name: facts_streams_stream_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.facts_streams_stream_id_seq', 1, false);


--
-- Name: stg_spotify_raw_raw_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stg_spotify_raw_raw_id_seq', 1, false);


--
-- Name: dim_artists dim_artists_artist_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_artists
    ADD CONSTRAINT dim_artists_artist_id_key UNIQUE (artist_id);


--
-- Name: dim_artists dim_artists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_artists
    ADD CONSTRAINT dim_artists_pkey PRIMARY KEY (artist_key);


--
-- Name: dim_tracks dim_tracks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_tracks
    ADD CONSTRAINT dim_tracks_pkey PRIMARY KEY (track_key);


--
-- Name: dim_tracks dim_tracks_track_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_tracks
    ADD CONSTRAINT dim_tracks_track_id_key UNIQUE (track_id);


--
-- Name: dim_users dim_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_users
    ADD CONSTRAINT dim_users_pkey PRIMARY KEY (user_key);


--
-- Name: dim_users dim_users_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_users
    ADD CONSTRAINT dim_users_user_id_key UNIQUE (user_id);


--
-- Name: facts_streams facts_streams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facts_streams
    ADD CONSTRAINT facts_streams_pkey PRIMARY KEY (stream_id);


--
-- Name: stg_spotify_raw stg_spotify_raw_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stg_spotify_raw
    ADD CONSTRAINT stg_spotify_raw_pkey PRIMARY KEY (raw_id);


--
-- Name: facts_streams facts_streams_artist_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facts_streams
    ADD CONSTRAINT facts_streams_artist_key_fkey FOREIGN KEY (artist_key) REFERENCES public.dim_artists(artist_key);


--
-- Name: facts_streams facts_streams_track_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facts_streams
    ADD CONSTRAINT facts_streams_track_key_fkey FOREIGN KEY (track_key) REFERENCES public.dim_tracks(track_key);


--
-- Name: facts_streams facts_streams_user_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facts_streams
    ADD CONSTRAINT facts_streams_user_key_fkey FOREIGN KEY (user_key) REFERENCES public.dim_users(user_key);


--
-- PostgreSQL database dump complete
--

\unrestrict NgM4o9bNFb92DnU3IcV5KgkCs7WF85ZWzV8WvhdReJLa3oVmsbaGW9cYUMkAadP

