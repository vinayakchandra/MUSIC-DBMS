-- USE your DB
USE music_db;

-- Users
INSERT INTO users (username, email)
VALUES ('Alice', 'alice@example.com'),
       ('Bob', 'bob@example.com'),
       ('Charlie', 'charlie@example.com');

-- Playlists
INSERT INTO playlists (title, user_id)
VALUES ('Chill Vibes', 1),
       ('Workout Mix', 2),
       ('Study Beats', 3);

-- Songs
INSERT INTO songs (title, genre, duration)
VALUES ('Lofi Rain', 'Lofi', 180),
       ('Run Wild', 'EDM', 210),
       ('Focus Now', 'Instrumental', 240),
       ('Echoes', 'Pop', 200),
       ('Dreamstate', 'Ambient', 300);

-- Artists
INSERT INTO artists (name, country)
VALUES ('DJ Luna', 'USA'),
       ('EchoBoy', 'Canada'),
       ('Zenith', 'Germany'),
       ('Aurora Skies', 'Norway');

-- playlist_songs (linking songs to playlists)
INSERT INTO playlist_songs (playlist_id, song_id)
VALUES (1, 1), -- Chill Vibes: Lofi Rain
       (1, 5), -- Chill Vibes: Dreamstate
       (2, 2), -- Workout Mix: Run Wild
       (2, 4), -- Workout Mix: Echoes
       (3, 1), -- Study Beats: Lofi Rain
       (3, 3);
-- Study Beats: Focus Now

-- song_artists (linking songs to artists)
INSERT INTO song_artists (song_id, artist_id)
VALUES (1, 3), -- Lofi Rain by Zenith
       (2, 1), -- Run Wild by DJ Luna
       (3, 2), -- Focus Now by EchoBoy
       (4, 1), -- Echoes by DJ Luna
       (5, 4); -- Dreamstate by Aurora Skies
