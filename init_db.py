import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
  "INSERT INTO Users (UserID, Username, Email, Password) VALUES (?, ?, ?, ?)",
  (1, 'elnatan', 'elnatan@gmail.com', 'password123'))


cur.execute(
  "INSERT INTO Artist (ArtistID, Name, Nationality, Biography) VALUES (?, ?, ?, ?)",
  (1, 'Beyonce', 'American',
   'Beyonce Giselle Knowles-Carter is an American singer, songwriter, and actress.'
   ))

cur.execute(
  "INSERT INTO Artist (ArtistID, Name, Nationality, Biography) VALUES (?, ?, ?, ?)",
  (2, 'Ed Sheeran', 'British',
   'Edward Christopher Sheeran is an English singer, songwriter, musician, and record producer.'
   ))

cur.execute(
  "INSERT INTO Artist (ArtistID, Name, Nationality, Biography) VALUES (?, ?, ?, ?)",
  (3, 'Queen', 'British',
   'Queen are a British rock band formed in London in 1970.'))

cur.execute(
  "INSERT INTO Artist (ArtistID, Name, Nationality, Biography) VALUES (?, ?, ?, ?)",
  (4, 'Ariana Grande', 'American',
   'Ariana Grande-Butera is an American singer, songwriter, and actress.'))

cur.execute(
  "INSERT INTO Artist (ArtistID, Name, Nationality, Biography) VALUES (?, ?, ?, ?)",
  (5, 'Coldplay', 'British',
   'Coldplay are a British rock band formed in London in 1996.'))

cur.execute(
  "INSERT INTO Album (AlbumID, Title, ArtistID, Year) VALUES (?, ?, ?, ?)",
  (1, 'Lemonade', 1, 2016))

cur.execute(
  "INSERT INTO Album (AlbumID, Title, ArtistID, Year) VALUES (?, ?, ?, ?)",
  (2, 'Divide', 2, 2017))

cur.execute(
  "INSERT INTO Album (AlbumID, Title, ArtistID, Year) VALUES (?, ?, ?, ?)",
  (3, 'A Night at the Opera', 3, 1975))

cur.execute(
  "INSERT INTO Album (AlbumID, Title, ArtistID, Year) VALUES (?, ?, ?, ?)",
  (4, 'Sweetener', 4, 2018))

cur.execute(
  "INSERT INTO Album (AlbumID, Title, ArtistID, Year) VALUES (?, ?, ?, ?)",
  (5, 'A Head Full of Dreams', 5, 2015))

cur.execute(
  "INSERT INTO Song (SongID, Title, ArtistID, AlbumID, Year, Duration, Lyrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
  (1, 'Formation', 1, 1, 2016, '02:34',
   'Okay, ladies, now lets get in formation'))

cur.execute(
  "INSERT INTO Song (SongID, Title, ArtistID, AlbumID, Year, Duration, Lyrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
  (2, 'Shape of You', 2, 2, 2017, '02:31',
   'The club is not the best place to find a lover'))

cur.execute(
  "INSERT INTO Song (SongID, Title, ArtistID, AlbumID, Year, Duration, Lyrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
  (3, 'Bohemian Rhapsody', 3, 3, 1975, '03:54',
   'Is this the real life? Is this just fantasy?'))

cur.execute(
  "INSERT INTO Song (SongID, Title, ArtistID, AlbumID, Year, Duration, Lyrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
  (4, 'God Is a Woman', 4, 4, 2018, '02:37',
   'You, you love it how I move you'))

cur.execute(
  "INSERT INTO Song (SongID, Title, ArtistID, AlbumID, Year, Duration, Lyrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
  (5, 'Adventure of a Lifetime', 5, 5, 2015, '02:36',
   'Turn your magic on, to me she wouod say'))

cur.execute(
  "INSERT INTO Genre (GenreID, Name, Description) VALUES (?, ?, ?)",
  (1, 'R&B',
   'Rhythm and blues is a genre of popular music that originated in African American communities in the 1940s.'
   ))

cur.execute(
  "INSERT INTO Genre (GenreID, Name, Description) VALUES (?, ?, ?)",
  (2, 'Pop',
   'Pop music is a genre of popular music that originated in the mid-1950s.'))

cur.execute(
  "INSERT INTO Genre (GenreID, Name, Description) VALUES (?, ?, ?)",
  (3, 'Rock',
   'Rock music is a genre of popular music that originated as "rock and roll" in the United States in the early 1950s.'
   ))

cur.execute(
  "INSERT INTO Genre (GenreID, Name, Description) VALUES (?, ?, ?)",
  (4, 'Hip hop',
   'Hip hop is a genre of music that originated in African American and Latinx communities in the Bronx, New York City, in the 1970s.'
   ))

cur.execute(
  "INSERT INTO Genre (GenreID, Name, Description) VALUES (?, ?, ?)",
  (5, 'Country',
   'Country music is a genre of American popular music that originated in the Southern United States in the early 1920s.'
   ))

cur.execute(
  "INSERT INTO Playlist (PlaylistID, Title, Description, UserID, TotalDuration) VALUES (?, ?, ?, ?, ?)",
  (1, 'Summer Vibes', 'The perfect playlist for sunny days and warm nights.',
   1, '02:34'))

cur.execute(
  "INSERT INTO Playlist (PlaylistID, Title, Description, UserID, TotalDuration) VALUES (?, ?, ?, ?, ?)",
  (2, 'Throwback Jams', 'Relive the good old days with these classic hits.', 1,
   '02:31'))

cur.execute(
  "INSERT INTO Playlist (PlaylistID, Title, Description, UserID, TotalDuration) VALUES (?, ?, ?, ?, ?)",
  (3, 'Workout Mix',
   'Get pumped up and crush your fitness goals with these high-energy tracks.',
   1, '03:54'))

cur.execute(
  "INSERT INTO Playlist (PlaylistID, Title, Description, UserID, TotalDuration) VALUES (?, ?, ?, ?, ?)",
  (4, 'Chill Out', 'Unwind and relax with these soothing melodies.', 1,
   '02:37'))

cur.execute(
  "INSERT INTO Playlist (PlaylistID, Title, Description, UserID, TotalDuration) VALUES (?, ?, ?, ?, ?)",
  (5, 'Party Time',
   'Get the party started with these upbeat and danceable tunes.', 1, '02:36'))

cur.execute(
  "INSERT INTO SongGenre (SongID, GenreID, Description) VALUES (?, ?, ?)",
  (5, 1, 'R&B'))

cur.execute(
  "INSERT INTO SongGenre (SongID, GenreID, Description) VALUES (?, ?, ?)",
  (2, 2, 'Pop'))

cur.execute(
  "INSERT INTO SongGenre (SongID, GenreID, Description) VALUES (?, ?, ?)",
  (3, 3, 'Rock'))

cur.execute(
  "INSERT INTO SongGenre (SongID, GenreID, Description) VALUES (?, ?, ?)",
  (4, 1, 'R&B'))

cur.execute(
  "INSERT INTO SongGenre (SongID, GenreID, Description) VALUES (?, ?, ?)",
  (5, 3, 'Rock'))

cur.execute(
  "INSERT INTO AlbumSong (AlbumID, SongID, TrackNumber) VALUES (?, ?, ?)",
  (1, 1, 1))

cur.execute(
  "INSERT INTO AlbumSong (AlbumID, SongID, TrackNumber) VALUES (?, ?, ?)",
  (2, 2, 2))

cur.execute(
  "INSERT INTO AlbumSong (AlbumID, SongID, TrackNumber) VALUES (?, ?, ?)",
  (3, 3, 3))

cur.execute(
  "INSERT INTO AlbumSong (AlbumID, SongID, TrackNumber) VALUES (?, ?, ?)",
  (4, 4, 4))

cur.execute(
  "INSERT INTO AlbumSong (AlbumID, SongID, TrackNumber) VALUES (?, ?, ?)",
  (5, 5, 5))

cur.execute(
  "INSERT INTO ArtistAlbum (ArtistID, AlbumID, ReleaseDate) VALUES (?, ?, ?)",
  (1, 1, '2016-04-23'))

cur.execute(
  "INSERT INTO ArtistAlbum (ArtistID, AlbumID, ReleaseDate) VALUES (?, ?, ?)",
  (2, 2, '2017-03-03'))

cur.execute(
  "INSERT INTO ArtistAlbum (ArtistID, AlbumID, ReleaseDate) VALUES (?, ?, ?)",
  (3, 3, '1975-11-21'))

cur.execute(
  "INSERT INTO ArtistAlbum (ArtistID, AlbumID, ReleaseDate) VALUES (?, ?, ?)",
  (4, 4, '2018-08-17'))

cur.execute(
  "INSERT INTO ArtistAlbum (ArtistID, AlbumID, ReleaseDate) VALUES (?, ?, ?)",
  (5, 5, '2015-12-04'))

cur.execute(
  "INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)",
  (1, 1, '2023-04-15'))

cur.execute(
  "INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)",
  (2, 2, '2023-04-16'))

cur.execute(
  "INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)",
  (3, 3, '2023-04-17'))

cur.execute(
  "INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)",
  (4, 4, '2023-04-18'))

cur.execute(
  "INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)",
  (5, 5, '2023-04-19'))

connection.commit()
connection.close()
