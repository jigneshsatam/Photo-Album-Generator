CREATE TABLE IF NOT EXISTS userinfo
(
    id serial PRIMARY KEY,
    username character varying(50) COLLATE pg_catalog."default",
    pwd character varying(50) COLLATE pg_catalog."default",
    firstname character varying(50) COLLATE pg_catalog."default",
    lastname character varying(50) COLLATE pg_catalog."default",
    usertype character varying(50) COLLATE pg_catalog."default"
);
