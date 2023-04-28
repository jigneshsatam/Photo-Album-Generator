CREATE TABLE IF NOT EXISTS userinfo
(
    id serial PRIMARY KEY,
    username character varying(50),
    pwd character varying(50),
    firstname character varying(50),
    lastname character varying(50),
    usertype character varying(50)
);

INSERT INTO userinfo(username, pwd, firstname, lastname, usertype)
VALUES('defaultuser', 'password', 'Default', 'User', 'admin');

CREATE TABLE IF NOT EXISTS imgdirectories
(
    id serial PRIMARY KEY,
    userid integer,
    dirpath text,

    CONSTRAINT FK_user FOREIGN KEY(userid)
        REFERENCES userinfo(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS photo(
  photo_id SERIAL PRIMARY KEY,
  photo_directory INT NOT NULL,
  photo_path TEXT NOT NULL
 
  -- CONSTRAINT FK_userinfo FOREIGN KEY(user_id) REFERENCES userinfo(id) ON DELETE CASCADE,
  -- CONSTRAINT FK_imgdirectories FOREIGN KEY(photo_directory) REFERENCES imgdirectories(id),
  -- CONSTRAINT FK_tags FOREIGN KEY(tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag(
  tag_id SERIAL PRIMARY KEY,
  tag TEXT NOT NULL

  -- CONSTRAINT FK_userifno FOREIGN KEY(user_id) REFERENCES userinfo(id) ON DELETE CASCADE,
  -- CONSTRAINT FK_photos FOREIGN KEY(foto_id) REFERENCES photos(photo_id) ON DELETE CASCADE,
  -- CONSTRAINT FK_photos FOREIGN KEY(foto_dir) REFERENCES photos(photo_directory) ON DELETE CASCADE    
);

CREATE TABLE IF NOT EXISTS tagging(
  tagging_id  SERIAL PRIMARY KEY,
  tag_id INTEGER NOT NULL,
  img_id INTEGER NOT NULL
);


