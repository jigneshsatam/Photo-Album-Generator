CREATE TABLE IF NOT EXISTS userinfo
(
    id serial PRIMARY KEY,
    user_name character varying(50),
    password character varying(50),
    first_name character varying(50),
    last_name character varying(50),
    user_type character varying(50),
    email character varying(255)
);

CREATE TABLE IF NOT EXISTS password_reset_tokens
(
    id serial PRIMARY KEY,
    user_id integer,
    token character varying(255),
    expiration_time timestamp,
    CONSTRAINT FK_user FOREIGN KEY(user_id)
        REFERENCES userinfo(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS imgdirectories
(
    id serial PRIMARY KEY,
    user_id integer,
    dir_path text,

    CONSTRAINT FK_user FOREIGN KEY(user_id)
        REFERENCES userinfo(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS photos(
  photo_id SERIAL PRIMARY KEY,
  photo_directory TEXT NOT NULL,
  photo_path TEXT NOT NULL,
  user_id  INTEGER UNIQUE NOT NULL,
  tag_id  INTERGER UNIQUE,
  CONSTRAINT FK_userinfo FOREIGN KEY(user_id) REFERENCES userinfo(id) ON DELETE CASCADE,
  CONSTRAINT FK_imgdirectories FOREIGN KEY(photo_directory) REFERENCES imgdirectories(dir_path),
  CONSTRAINT FK_tags FOREIGN KEY(tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tags(
  tag_id SERIAL PRIMARY KEY,
  tag TEXT NOT NULL,
  user_id INTEGER UNIQUE NOT NULL,
  foto_id INTEGER UNIQUE NOT NULL,
  foto_dir TEXT NOT NULL,
  CONSTRAINT FK_user_info FOREIGN KEY(user_id) REFERENCES userinfo(id) ON DELETE CASCADE,
  CONSTRAINT FK_photos FOREIGN KEY(foto_id) REFERENCES photos(photo_id) ON DELETE CASCADE,
  CONSTRAINT FK_photos_dir FOREIGN KEY(foto_dir) REFERENCES photos(photo_directory) ON DELETE CASCADE    
);

INSERT INTO userinfo(user_name, password, first_name, last_name, user_type)
VALUES('defaultuser', 'password', 'Default', 'User', 'admin');