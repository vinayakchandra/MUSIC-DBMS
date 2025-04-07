CREATE DATABASE music_db;
USE music_db;

CREATE TABLE users
(
    id       INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100)        NOT NULL,
    email    VARCHAR(100) UNIQUE NOT NULL
# gender
);

CREATE TABLE playlists
(
    id      INT AUTO_INCREMENT PRIMARY KEY,
    title   VARCHAR(100) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
# date
);

CREATE TABLE songs
(
    id       INT AUTO_INCREMENT PRIMARY KEY,
    title    VARCHAR(100) NOT NULL,
    genre    VARCHAR(50),
    duration INT
);

CREATE TABLE artists
(
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    country VARCHAR(100)
);

CREATE TABLE playlist_songs
(
    playlist_id INT,
    song_id     INT,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
);

CREATE TABLE song_artists
(
    song_id   INT,
    artist_id INT,
    PRIMARY KEY (song_id, artist_id),
    FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE CASCADE
);
