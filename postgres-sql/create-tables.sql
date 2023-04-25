CREATE TABLE IF NOT EXISTS userinfo
(
    id serial PRIMARY KEY,
    username character varying(50),
    pwd character varying(50),
    firstname character varying(50),
    lastname character varying(50),
    usertype character varying(50)
);

CREATE TABLE IF NOT EXISTS imgdirectories
(
    id serial PRIMARY KEY,
    userid integer,
    dirpath text,

    CONSTRAINT FK_user FOREIGN KEY(userid)
        REFERENCES userinfo(id)
        ON DELETE CASCADE
);

INSERT INTO userinfo(username, pwd, firstname, lastname, usertype)
VALUES('defaultuser', 'password', 'Default', 'User', 'admin');
