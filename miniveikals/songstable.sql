CREATE TABLE allsongs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    length TEXT,
    image TEXT,
    authors TEXT,
    album_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 1 FROM hourswere;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 2 FROM asides;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 3 FROM bsides;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 4 FROM abysskiss;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 5 FROM instrumentals;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 6 FROM songs;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 7 FROM brightfuture;

INSERT INTO allsongs (name, length, image, authors, album_id)
SELECT name, length, image, authors, 8 FROM revolutionhall;

CREATE TABLE details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER,
    album_info TEXT,
    FOREIGN KEY (album_id) REFERENCES albums(id)
);