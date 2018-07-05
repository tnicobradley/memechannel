--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4
-- Dumped by pg_dump version 10.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: objectcount; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.objectcount (
    id integer NOT NULL,
    selfidentifier character varying(255) NOT NULL,
    postcount integer NOT NULL,
    usercount integer NOT NULL
);


ALTER TABLE public.objectcount OWNER TO postgres;

--
-- Name: objectcount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.objectcount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.objectcount_id_seq OWNER TO postgres;

--
-- Name: objectcount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.objectcount_id_seq OWNED BY public.objectcount.id;


--
-- Name: post; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.post (
    id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    title character varying(255) NOT NULL,
    text text NOT NULL,
    image text NOT NULL,
    user_id character varying(255) NOT NULL,
    last_reply timestamp without time zone NOT NULL,
    nsfw boolean NOT NULL,
    eternal boolean NOT NULL,
    replies integer NOT NULL
);


ALTER TABLE public.post OWNER TO postgres;

--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_id_seq OWNER TO postgres;

--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


--
-- Name: reply; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reply (
    id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    text text NOT NULL,
    post_id integer NOT NULL,
    image text NOT NULL,
    user_id character varying(255) NOT NULL,
    nsfw boolean NOT NULL
);


ALTER TABLE public.reply OWNER TO postgres;

--
-- Name: reply_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reply_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reply_id_seq OWNER TO postgres;

--
-- Name: reply_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reply_id_seq OWNED BY public.reply.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id character varying(255) NOT NULL,
    tagname character varying(80) NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    is_admin boolean NOT NULL,
    is_master boolean NOT NULL,
    password character varying(255) NOT NULL,
    nsfwfilter boolean NOT NULL,
    reset_token character varying(255) NOT NULL,
    last_reset timestamp without time zone NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: userblock; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userblock (
    id integer NOT NULL,
    blocking_id character varying(255) NOT NULL,
    blocker_id character varying(255) NOT NULL
);


ALTER TABLE public.userblock OWNER TO postgres;

--
-- Name: userblock_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.userblock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.userblock_id_seq OWNER TO postgres;

--
-- Name: userblock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.userblock_id_seq OWNED BY public.userblock.id;


--
-- Name: userinfo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userinfo (
    id integer NOT NULL,
    key character varying(64) NOT NULL,
    value character varying(64) NOT NULL,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public.userinfo OWNER TO postgres;

--
-- Name: userinfo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.userinfo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.userinfo_id_seq OWNER TO postgres;

--
-- Name: userinfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.userinfo_id_seq OWNED BY public.userinfo.id;


--
-- Name: userlink; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userlink (
    id integer NOT NULL,
    following_id character varying(255) NOT NULL,
    follower_id character varying(255) NOT NULL
);


ALTER TABLE public.userlink OWNER TO postgres;

--
-- Name: userlink_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.userlink_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.userlink_id_seq OWNER TO postgres;

--
-- Name: userlink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.userlink_id_seq OWNED BY public.userlink.id;


--
-- Name: objectcount id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objectcount ALTER COLUMN id SET DEFAULT nextval('public.objectcount_id_seq'::regclass);


--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: reply id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reply ALTER COLUMN id SET DEFAULT nextval('public.reply_id_seq'::regclass);


--
-- Name: userblock id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userblock ALTER COLUMN id SET DEFAULT nextval('public.userblock_id_seq'::regclass);


--
-- Name: userinfo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userinfo ALTER COLUMN id SET DEFAULT nextval('public.userinfo_id_seq'::regclass);


--
-- Name: userlink id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userlink ALTER COLUMN id SET DEFAULT nextval('public.userlink_id_seq'::regclass);


--
-- Data for Name: objectcount; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.objectcount (id, selfidentifier, postcount, usercount) FROM stdin;
1	counter	1	4
\.


--
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.post (id, date, title, text, image, user_id, last_reply, nsfw, eternal, replies) FROM stdin;
1	2018-06-22 03:13:05.77569	One Post To Rule Them All	One post to find them \n one post to bring them all \n and in the darkness bind them\n in the land of imgin where the shadows lie.	onering.jpg	1	2018-06-22 03:16:26.322546	f	t	1
\.


--
-- Data for Name: reply; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reply (id, date, text, post_id, image, user_id, nsfw) FROM stdin;
1	2018-06-22 03:16:26.322546	WE WANTS IT!!!!!!!!!!!!!!!!!!!!!!!!	1	None	4	f
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, tagname, username, email, is_admin, is_master, password, nsfwfilter, reset_token, last_reset) FROM stdin;
1	MITHRANDIR	Mithrandir	greatestwizard@middleearth.com	t	t	b371dbc4b0268fd4fb467c755690433d1c50348b944b696087a8700a4235217e	f		2018-06-22 03:13:05.760835
2	FEANOR	Fëanor	muhsilmarils@valinor.com	t	t	b371dbc4b0268fd4fb467c755690433d1c50348b944b696087a8700a4235217e	f		2018-06-22 03:13:05.762836
3	DICK	Dick	blah@blah.com	t	t	b371dbc4b0268fd4fb467c755690433d1c50348b944b696087a8700a4235217e	f		2018-06-22 03:13:05.763824
4	SMEAGOL	Smeagol	fc948746f5	f	f	a17c48bec3b49e16ddca15c06e1bcf161e6390b064bbb10285d066f6587ba7ce	f	71093	2018-06-22 03:16:13.271892
\.


--
-- Data for Name: userblock; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userblock (id, blocking_id, blocker_id) FROM stdin;
1	1	3
2	3	1
\.


--
-- Data for Name: userinfo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userinfo (id, key, value, user_id) FROM stdin;
\.


--
-- Data for Name: userlink; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userlink (id, following_id, follower_id) FROM stdin;
1	1	2
2	2	1
\.


--
-- Name: objectcount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.objectcount_id_seq', 1, true);


--
-- Name: post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.post_id_seq', 8, true);


--
-- Name: reply_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reply_id_seq', 3, true);


--
-- Name: userblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.userblock_id_seq', 2, true);


--
-- Name: userinfo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.userinfo_id_seq', 1, false);


--
-- Name: userlink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.userlink_id_seq', 2, true);


--
-- Name: objectcount objectcount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objectcount
    ADD CONSTRAINT objectcount_pkey PRIMARY KEY (id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: reply reply_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reply
    ADD CONSTRAINT reply_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: userblock userblock_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userblock
    ADD CONSTRAINT userblock_pkey PRIMARY KEY (id);


--
-- Name: userinfo userinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userinfo
    ADD CONSTRAINT userinfo_pkey PRIMARY KEY (id);


--
-- Name: userlink userlink_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userlink
    ADD CONSTRAINT userlink_pkey PRIMARY KEY (id);


--
-- Name: post_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX post_user_id ON public.post USING btree (user_id);


--
-- Name: reply_post_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX reply_post_id ON public.reply USING btree (post_id);


--
-- Name: reply_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX reply_user_id ON public.reply USING btree (user_id);


--
-- Name: user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX user_email ON public."user" USING btree (email);


--
-- Name: userblock_blocker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userblock_blocker_id ON public.userblock USING btree (blocker_id);


--
-- Name: userblock_blocker_id_blocking_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX userblock_blocker_id_blocking_id ON public.userblock USING btree (blocker_id, blocking_id);


--
-- Name: userblock_blocking_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userblock_blocking_id ON public.userblock USING btree (blocking_id);


--
-- Name: userinfo_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userinfo_user_id ON public.userinfo USING btree (user_id);


--
-- Name: userlink_follower_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userlink_follower_id ON public.userlink USING btree (follower_id);


--
-- Name: userlink_follower_id_following_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX userlink_follower_id_following_id ON public.userlink USING btree (follower_id, following_id);


--
-- Name: userlink_following_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userlink_following_id ON public.userlink USING btree (following_id);


--
-- Name: post post_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: reply reply_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reply
    ADD CONSTRAINT reply_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.post(id);


--
-- Name: reply reply_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reply
    ADD CONSTRAINT reply_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: userblock userblock_blocker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userblock
    ADD CONSTRAINT userblock_blocker_id_fkey FOREIGN KEY (blocker_id) REFERENCES public."user"(id);


--
-- Name: userblock userblock_blocking_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userblock
    ADD CONSTRAINT userblock_blocking_id_fkey FOREIGN KEY (blocking_id) REFERENCES public."user"(id);


--
-- Name: userinfo userinfo_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userinfo
    ADD CONSTRAINT userinfo_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: userlink userlink_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userlink
    ADD CONSTRAINT userlink_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public."user"(id);


--
-- Name: userlink userlink_following_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userlink
    ADD CONSTRAINT userlink_following_id_fkey FOREIGN KEY (following_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

