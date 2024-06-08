DROP TABLE IF EXISTS photos_posts;
CREATE TABLE photos_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    path TEXT,
    status BOOLEAN
 );

DROP TABLE IF EXISTS photos_predictions;
CREATE TABLE photos_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_foreign_key INT REFERENCES photos_posts(id),
    top_prediction REAL,
    trouser_prediction REAL,
    pullover_prediction REAL,
    dress_prediction REAL,
    coat_prediction REAL,
    sandal_prediction REAL,
    shirt_prediction REAL,
    sneaker_prediction REAL,
    bag_prediction REAL,
    ankle_boot_prediction REAL
);
