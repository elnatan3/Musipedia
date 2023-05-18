DROP TABLE IF EXISTS Song;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS SongGenre;
DROP TABLE IF EXISTS AlbumSong;
DROP TABLE IF EXISTS ArtistAlbum;
DROP TABLE IF EXISTS PlaylistSong;
DROP TABLE IF EXISTS Beats;

CREATE TABLE Beats (
  BeatID INTEGER PRIMARY KEY,
  Title VARCHAR(255),
  Duration VARCHAR(255),
  Description VARCHAR(255)
);

  
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(255),
    Email VARCHAR(255),
    Password VARCHAR(255)
);


CREATE TABLE Song (
    SongID INTEGER PRIMARY KEY,
    Title VARCHAR(255),
    ArtistID INT,
    AlbumID INT,
    Year INT,
    Duration VARCHAR(255),
    Lyrics TEXT,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

CREATE TABLE Artist (
    ArtistID INTEGER PRIMARY KEY,
    Name VARCHAR(255),
    Nationality VARCHAR(255),
    Biography TEXT
);

CREATE TABLE Album (
    AlbumID INTEGER PRIMARY KEY,
    Title VARCHAR(255),
    ArtistID INT,
    Year INT,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID)
);

CREATE TABLE Genre (
    GenreID INTEGER PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT
);

CREATE TABLE Playlist (
    PlaylistID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(255),
    Description TEXT,
    UserID INTEGER,
    TotalDuration VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);


CREATE TABLE SongGenre (
    SongID INTEGER,
    GenreID INTEGER,
    Description VARCHAR(255),
    PRIMARY KEY (SongID, GenreID),
    FOREIGN KEY (SongID) REFERENCES Song(SongID),
    FOREIGN KEY (GenreID) REFERENCES Genre(GenreID)
);

CREATE TABLE AlbumSong (
    AlbumID INTEGER,
    SongID INTEGER,
    TrackNumber INTEGER,
    PRIMARY KEY (AlbumID, SongID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID),
    FOREIGN KEY (SongID) REFERENCES Song(SongID)
);

CREATE TABLE ArtistAlbum (
    ArtistID INTEGER,
    AlbumID INTEGER,
    ReleaseDate DATE,
    PRIMARY KEY (ArtistID, AlbumID),
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

CREATE TABLE PlaylistSong (
    PlaylistID INTEGER,
    SongID INTEGER,
    DateAdded DATE,
    PRIMARY KEY (PlaylistID, SongID),
    FOREIGN KEY (PlaylistID) REFERENCES Playlist(PlaylistID),
    FOREIGN KEY (SongID) REFERENCES Song(SongID)
);


-- Add 5 rows to Song table
INSERT INTO Song (SongID, Title, ArtistID, AlbumID, Year, Duration, Lyrics) 
VALUES 
(6, 'Someone Like You', 6, 6, 2011, '04:45', 'I heard that you''re settled down'),
(7, 'Mr. Brightside', 7, 7, 2003, '03:43', 'Coming out of my cage'),
(8, 'Stairway to Heaven', 8, 8, 1971, '08:02', 'There''s a lady who''s sure all that glitters is gold'),
(9, 'I Will Always Love You', 9, 9, 1992, '04:31', 'If I should stay, I would only be in your way');

-- Add 5 rows to Artist table
INSERT INTO Artist (ArtistID, Name, Nationality, Biography)
VALUES
(6, 'Adele', 'British', 'Adele Laurie Blue Adkins MBE is an English singer-songwriter.'),
(7, 'The Killers', 'American', 'The Killers are an American rock band formed in Las Vegas, Nevada, in 2001.'),
(8, 'Led Zeppelin', 'British', 'Led Zeppelin were an English rock band formed in London in 1968.'),
(9, 'Whitney Houston', 'American', 'Whitney Elizabeth Houston was an American singer and actress.');

-- Add 5 rows to Album table
INSERT INTO Album (AlbumID, Title, ArtistID, Year)
VALUES
(6, '21', 6, 2011),
(7, 'Hot Fuss', 7, 2004),
(8, 'Led Zeppelin IV', 8, 1971),
(9, 'The Bodyguard', 9, 1992);

-- Add 5 rows to Genre table
INSERT INTO Genre (GenreID, Name, Description)
VALUES
(6, 'Electronic', 'Electronic music is music that employs electronic musical instruments, digital instruments, or circuitry-based music technology.'),
(7, 'Classical', 'Classical music is art music produced or rooted in the traditions of Western culture, including both liturgical and secular music.'),
(8, 'Jazz', 'Jazz is a music genre that originated in the African-American communities of New Orleans, United States, in the late 19th and early 20th centuries.'),
(9, 'Reggae', 'Reggae is a music genre that originated in Jamaica in the late 1960s and is characterized by its distinctive rhythm and basslines.');

-- Add 5 rows to SongGenre table
INSERT INTO SongGenre (SongID, GenreID, Description)
VALUES
(6, 2, 'Pop'),
(7, 3, 'Rock'),
(8, 3, 'Rock'),
(9, 1, 'R&B');

INSERT INTO ArtistAlbum (ArtistID, AlbumID, ReleaseDate)
VALUES
(6, 6, '2011-01-24'),
(7, 7, '2004-06-07'),
(8, 8, '1971-11-08'),
(9, 9, '1992-11-17');

INSERT INTO AlbumSong (AlbumID, SongID, TrackNumber)
VALUES
(6, 6, 2),
(7, 7, 3),
(8, 8, 1),
(9, 9, 2);

INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (1, 'House', '04:02', 'House beats typically use a kick drum on every downbeat, with snare or clap sounds on the 2nd and 4th beat of each bar, and hi-hats or cymbals on every eighth note.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (2, 'Trap', '02:44', 'Trap beats are a subgenre of hip-hop and is characterized by heavy, distorted basslines, crisp snares, and prominent hi-hats, often played at a slower tempo than other hip-hop subgenres.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (3, 'Electronic', '03:08', 'Electronic beats are characterized by their repetitive, percussive sound, and are created using different electronic instruments such as synthesizers, drum machines, and samplers.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (4, 'Bass', '02:77', 'Bass beats can be characterized by its heavy, often distorted basslines, intricate percussion patterns, and use of synthesizers and other electronic instruments.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (5, 'Dubstep', '02:56', 'Dubstep beats are characterized by its heavy, deep bass lines, complex rhythms, and use of effects such as wobble bass, which create a "wobbly" or "vibrating" sound.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (6, 'Drumstep', '03:00', 'Drumstep often features heavy and aggressive basslines, chopped up vocal samples, and complex drum patterns that are a mix of fast-paced drum and bass beats and half-time dubstep beats.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (7, 'Hardstyle', '03:55', 'Hardstyle is characterized by heavy bass and drum rhythms, high-energy melodies, and distorted, chopped-up vocal samples.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (8, 'Chill', '02:42', 'Chill beats is generally slow to mid-tempo, with a focus on atmospheric sounds, soft melodies, and gentle rhythms.');
INSERT INTO Beats(BeatID, Title, Duration, Description) VALUES (9, 'Hip Hop', '02:32', 'Hip hop beats usually consist of a drum loop or sample, a bassline, and various other melodic elements such as samples, synths, and keyboards.');