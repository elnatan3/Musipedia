import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, jsonify, session
import requests
from datetime import date
import random

# ...

# Create a flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'your secret key'


def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn


# Index page (now using the index.html file)
@app.route('/')
def index():
  conn = get_db_connection()
  # Get the UserID of the logged-in user from the session variable
  user_id = session.get('user_id')
  # Retrieve a list of genres from the database
  genres = conn.execute("SELECT * FROM Genre").fetchall()
  playlists = conn.execute(
    'SELECT Playlist.PlaylistID, Title, Description, TotalDuration, COUNT(PlaylistSong.SongID) AS TotalSongs '
    'FROM Playlist '
    'JOIN Users ON Playlist.UserID = Users.UserID '
    'LEFT JOIN PlaylistSong ON Playlist.PlaylistID = PlaylistSong.PlaylistID '
    'WHERE Playlist.UserID = ? '
    'GROUP BY Playlist.PlaylistID', (user_id, )).fetchall()
  beats = conn.execute(
    'SELECT Title, Duration, Description FROM Beats').fetchall()

  # Pick a random genre
  random_genre = random.choice(genres)
  conn.close()

  return render_template('index.html',
                         random_genre=random_genre,
                         genres=genres,
                         playlists=playlists,
                         beats=beats)


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/song/')
def getSong():
  conn = get_db_connection()
  songs = conn.execute(
    'SELECT Song.*, Artist.Name AS ArtistName, Album.Title AS AlbumTitle FROM Song JOIN Artist ON Song.ArtistID = Artist.ArtistID JOIN Album ON Song.AlbumID = Album.AlbumID'
  ).fetchall()
  conn.close()

  return render_template('songs.html', songs=songs)


@app.route('/explore_songs')
def explore_songs():
  return render_template('explore.html')


@app.route('/beat')
def beat():
  conn = get_db_connection()
  beats = conn.execute(
    'SELECT Title, Duration, Description FROM Beats').fetchall()
  conn.close()

  # render the beats.html template with the beats data
  return render_template('beats.html', beats=beats)


@app.route('/song/<int:song_id>/playlists')
def view_playlists_for_song(song_id):
  conn = get_db_connection()
  user_id = session.get('user_id')

  if not user_id:
    conn.close()
    return redirect(url_for('existing_user'))

  song = conn.execute('SELECT * FROM Song WHERE SongID = ?',
                      (song_id, )).fetchone()

  playlists = conn.execute(
    'SELECT Playlist.*, PlaylistSong.DateAdded FROM Playlist JOIN PlaylistSong ON Playlist.PlaylistID = PlaylistSong.PlaylistID JOIN Song ON PlaylistSong.SongID = Song.SongID JOIN Users ON Playlist.UserID = Users.UserID WHERE Song.SongID = ? AND Users.UserID = ?',
    (song_id, user_id)).fetchall()

  conn.close()

  return render_template('song_playlist.html',
                         playlists=playlists,
                         song=song,
                         song_id=song_id)


@app.route('/song/<int:song_id>/add-to-playlist')
def add_song_to_playlist(song_id):
  conn = get_db_connection()
  song = conn.execute('SELECT * FROM Song WHERE SongID = ?',
                      (song_id, )).fetchone()
  user_id = session.get('user_id')

  if not user_id:
    conn.close()
    return redirect(url_for('existing_user'))

  playlists = conn.execute(
    'SELECT * FROM Playlist WHERE UserID = ? AND PlaylistID NOT IN (SELECT PlaylistID FROM PlaylistSong WHERE SongID = ?)',
    (user_id, song_id)).fetchall()

  conn.close()
  return render_template('add_to_playlist.html',
                         song=song,
                         song_id=song_id,
                         playlists=playlists)


@app.route('/playlist/<int:playlist_id>/add-song/<int:song_id>')
def add_song_to_playlist_action(playlist_id, song_id):
  conn = get_db_connection()

  # Get the playlist's current total duration
  playlist = conn.execute(
    'SELECT Title, TotalDuration FROM Playlist WHERE PlaylistID = ?',
    (playlist_id, )).fetchone()
  current_total_duration = playlist['TotalDuration']
  current_minutes, current_seconds = current_total_duration.split(':')
  current_total_seconds = int(current_minutes) * 60 + int(current_seconds)

  # Get the song's duration
  song = conn.execute('SELECT Title, Duration FROM Song WHERE SongID = ?',
                      (song_id, )).fetchone()
  song_duration = song['Duration']

  # Convert song_duration from mm:ss format to seconds
  song_minutes, song_seconds = song_duration.split(':')
  song_total_seconds = int(song_minutes) * 60 + int(song_seconds)

  # Convert the total duration back to mm:ss format
  total_seconds = current_total_seconds + song_total_seconds
  total_minutes, total_seconds = divmod(total_seconds, 60)
  new_total_duration = '{:02d}:{:02d}'.format(total_minutes, total_seconds)

  conn.execute('UPDATE Playlist SET TotalDuration = ? WHERE PlaylistID = ?',
               (new_total_duration, playlist_id))

  # Add the song to the playlist
  conn.execute(
    'INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)',
    (playlist_id, song_id, date.today()))

  conn.commit()
  conn.close()
  flash(f"'{song['Title']}' is now added to '{playlist['Title']}' playlist!")
  return redirect(url_for('getSong', playlist_id=playlist_id, song_id=song_id))


@app.route('/playlist/<int:playlist_id>/remove-song/<int:song_id>')
def remove_song_from_playlist(playlist_id, song_id):
  conn = get_db_connection()
  # Remove the song from the playlist
  conn.execute('DELETE FROM PlaylistSong WHERE PlaylistID = ? AND SongID = ?',
               (playlist_id, song_id))

  # Calculate the new total duration of the playlist
  playlist = conn.execute(
    'SELECT Title, TotalDuration FROM Playlist WHERE PlaylistID = ?',
    (playlist_id, )).fetchone()
  current_total_duration = playlist['TotalDuration']
  current_minutes, current_seconds = current_total_duration.split(':')
  current_total_seconds = int(current_minutes) * 60 + int(current_seconds)

  # Get the song's duration
  song = conn.execute('SELECT Title, Duration FROM Song WHERE SongID = ?',
                      (song_id, )).fetchone()
  song_duration = song['Duration']

  # Convert song_duration from mm:ss format to seconds
  minutes, seconds = song_duration.split(':')
  song_duration_seconds = int(minutes) * 60 + int(seconds)

  # Update the playlist's total duration
  new_total_duration_seconds = current_total_seconds - song_duration_seconds
  if new_total_duration_seconds == 0:
    new_total_duration = '00:00'
  else:
    new_minutes = new_total_duration_seconds // 60
    new_seconds = new_total_duration_seconds % 60
    new_total_duration = '{:02d}:{:02d}'.format(new_minutes, new_seconds)
  conn.execute('UPDATE Playlist SET TotalDuration = ? WHERE PlaylistID = ?',
               (new_total_duration, playlist_id))

  conn.commit()
  conn.close()
  flash(
    f"'{song['Title']}' is now removed from '{playlist['Title']}' playlist!")
  return redirect(
    url_for('view_playlists_for_song',
            playlist_id=playlist_id,
            song_id=song_id))


@app.route('/like_song/<int:song_id>')
def like_song(song_id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
    "SELECT Title, ArtistID, AlbumID, Year, Duration FROM Song WHERE SongID=?",
    (song_id, ))
  song = cursor.fetchone()
  if song is None:
    return "Song not found"

  user_id = session.get('user_id')

  if not user_id:

    conn.close()
    return redirect(url_for('existing_user'))

  cursor.execute(
    "SELECT PlaylistID FROM Playlist WHERE Title='Favorite songs' AND UserID=?",
    (user_id, ))
  playlist = cursor.fetchone()
  if playlist is None:

    song = conn.execute('SELECT Duration FROM Song WHERE SongID = ?',
                        (song_id, )).fetchone()
    song_duration = song['Duration']

    cursor.execute(
      "INSERT INTO Playlist (UserID, Title, Description, TotalDuration) VALUES (?, ?, ?, ?)",
      (user_id, 'Favorite songs', 'Your favorite songs playlist',
       song_duration))
    playlist_id = cursor.lastrowid

  else:
    playlist_id = playlist[0]

    playlist = conn.execute(
      'SELECT TotalDuration FROM Playlist WHERE PlaylistID = ?',
      (playlist_id, )).fetchone()
    current_total_duration = playlist['TotalDuration']
    current_minutes, current_seconds = current_total_duration.split(':')
    current_total_seconds = int(current_minutes) * 60 + int(current_seconds)

    song = conn.execute('SELECT Duration FROM Song WHERE SongID = ?',
                        (song_id, )).fetchone()
    song_duration = song['Duration']

    song_minutes, song_seconds = song_duration.split(':')
    song_total_seconds = int(song_minutes) * 60 + int(song_seconds)

    total_seconds = current_total_seconds + song_total_seconds
    total_minutes, total_seconds = divmod(total_seconds, 60)
    new_total_duration = '{:02d}:{:02d}'.format(total_minutes, total_seconds)

    conn.execute('UPDATE Playlist SET TotalDuration = ? WHERE PlaylistID = ?',
                 (new_total_duration, playlist_id))

  cursor.execute("SELECT * FROM PlaylistSong WHERE PlaylistID=? AND SongID=?",
                 (playlist_id, song_id))
  playlist_song = cursor.fetchone()
  if playlist_song is None:

    conn.execute(
      'INSERT INTO PlaylistSong (PlaylistID, SongID, DateAdded) VALUES (?, ?, ?)',
      (playlist_id, song_id, date.today()))
    conn.commit()

    cursor.execute("SELECT Title FROM Song WHERE SongID=?", (song_id, ))
    song = cursor.fetchone()

    flash(f"'{song['Title']}' is now add to you Favorite playlist!")
  else:

    cursor.execute("SELECT Title FROM Song WHERE SongID=?", (song_id, ))
    song = cursor.fetchone()
    flash(
      f"The song '{song['Title']}' is already in your favorite songs playlist."
    )
  conn.close()

  # Redirect back to the songs page
  return redirect(url_for('getSong'))


@app.route('/playlist/')
def getPlaylist():
  conn = get_db_connection()

  user_id = session.get('user_id')

  if not user_id:

    conn.close()
    return redirect(url_for('existing_user'))

  playlists = conn.execute(
    'SELECT Playlist.PlaylistID, Title, Description, TotalDuration, COUNT(PlaylistSong.SongID) AS TotalSongs '
    'FROM Playlist '
    'JOIN Users ON Playlist.UserID = Users.UserID '
    'LEFT JOIN PlaylistSong ON Playlist.PlaylistID = PlaylistSong.PlaylistID '
    'WHERE Playlist.UserID = ? '
    'GROUP BY Playlist.PlaylistID', (user_id, )).fetchall()

  conn.close()
  return render_template('playlist.html', playlists=playlists)


@app.route('/playlist/<int:id>/songs/')
def get_playlist_songs(id):
  conn = get_db_connection()
  playlist = conn.execute(
    'SELECT PlaylistID, Title FROM Playlist WHERE PlaylistID = ?',
    (id, )).fetchone()

  if not playlist:
    abort(404)

  songs = conn.execute(
    'SELECT Song.SongID, Song.Title, Artist.Name AS ArtistName, Album.Title AS AlbumTitle, Song.Year, Duration, Lyrics FROM Song '
    'JOIN Artist ON Song.ArtistID = Artist.ArtistID '
    'LEFT JOIN Album ON Song.AlbumID = Album.AlbumID '
    'JOIN PlaylistSong ON Song.SongID = PlaylistSong.SongID '
    'WHERE PlaylistSong.PlaylistID = ? '
    'ORDER BY PlaylistSong.DateAdded DESC', (id, )).fetchall()

  conn.close()

  return render_template('playlist_songs.html', playlist=playlist, songs=songs)


@app.route('/playlist/<int:playlist_id>/song/<int:song_id>/remove',
           methods=['POST'])
def remove_from_playlist(playlist_id, song_id):
  conn = get_db_connection()

  conn.execute('DELETE FROM PlaylistSong WHERE PlaylistID = ? AND SongID = ?',
               (playlist_id, song_id))

  playlist = conn.execute(
    'SELECT Title, TotalDuration FROM Playlist WHERE PlaylistID = ?',
    (playlist_id, )).fetchone()
  current_total_duration = playlist['TotalDuration']
  current_minutes, current_seconds = current_total_duration.split(':')
  current_total_seconds = int(current_minutes) * 60 + int(current_seconds)

  song = conn.execute('SELECT Title, Duration FROM Song WHERE SongID = ?',
                      (song_id, )).fetchone()
  song_duration = song['Duration']

  minutes, seconds = song_duration.split(':')
  song_duration_seconds = int(minutes) * 60 + int(seconds)

  new_total_duration_seconds = current_total_seconds - song_duration_seconds
  if new_total_duration_seconds == 0:
    new_total_duration = '00:00'
    flash(
      f"'{song['Title']}' is now removed. Now you have no songs in this playlist!"
    )
  else:
    flash(
      f"'{song['Title']}' is now removed from '{playlist['Title']}' playlist!")
    new_minutes = new_total_duration_seconds // 60
    new_seconds = new_total_duration_seconds % 60
    new_total_duration = '{:02d}:{:02d}'.format(new_minutes, new_seconds)
  conn.execute('UPDATE Playlist SET TotalDuration = ? WHERE PlaylistID = ?',
               (new_total_duration, playlist_id))

  conn.commit()
  conn.close()

  return redirect(url_for('get_playlist_songs', id=playlist_id))


@app.route('/create_playlist/', methods=['GET', 'POST'])
def create_playlist():
  if request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    if not title:
      flash('Title is required!')
    elif not description:
      flash('Content is required!')
    else:
      conn = get_db_connection()

      user_id = session.get('user_id')

      if not user_id:
        conn.close()
        return redirect(url_for('existing_user'))
      existing_playlist = conn.execute(
        'SELECT * FROM Playlist WHERE UserID = ? AND Title = ?',
        (user_id, title)).fetchone()

      if existing_playlist:

        conn.close()
        flash('Playlist with this title already exists!', 'error')
        return redirect(url_for('getPlaylist'))
      conn.execute(
        'INSERT INTO Playlist (UserID, Title, Description, TotalDuration) VALUES (?, ?, ?, ?)',
        (user_id, title, description, '00:00'))
      conn.commit()
      conn.close()
      flash("Playlist created successfully!")
      return redirect(url_for('getPlaylist'))
  else:
    return render_template('create_playlist.html')


@app.route('/edit_playlist/<int:id>', methods=['GET', 'POST'])
def edit_playlist(id):
  conn = get_db_connection()
  playlist = conn.execute('SELECT * FROM Playlist WHERE PlaylistID = ?',
                          (id, )).fetchone()

  if request.method == 'POST':
    # Get form data
    title = request.form['title']
    description = request.form['description']
    if not title:
      flash('Title is required!')

    elif not description:
      flash('Content is required!')

    else:
      # Update data in database
      conn.execute(
        'UPDATE Playlist SET Title = ?, Description = ? WHERE PlaylistID = ?',
        (title, description, id))
      conn.commit()
      conn.close()
      flash(f"'{playlist['Title']}' is updated successfully!")

      # Redirect to playlist page
      return redirect(url_for('getPlaylist'))

  # Render the edit playlist page
  return render_template('edit_playlist.html', id=id, playlist=playlist)


@app.route('/delete_playlist/<int:id>', methods=['POST'])
def delete_playlist(id):
  conn = get_db_connection()
  playlist = conn.execute('SELECT * FROM Playlist WHERE PlaylistID = ?',
                          (id, )).fetchone()
  conn.execute('DELETE FROM Playlist WHERE PlaylistID = ?', (id, ))
  conn.commit()
  conn.close()
  flash('"{}" was successfully deleted!'.format(playlist['Title']))
  return redirect(url_for('getPlaylist'))


@app.route('/artist/', methods=['GET', 'POST'])
def getArtist():
  conn = get_db_connection()
  search = request.args.get('search')
  if search:
    artists = conn.execute(
      f"SELECT * FROM Artist WHERE Name LIKE '%{search}%'").fetchall()
  else:
    artists = conn.execute('SELECT * FROM Artist').fetchall()
  conn.close()
  return render_template('artist.html', artists=artists)


@app.route('/album/')
def getAlbum():
  conn = get_db_connection()
  albums = conn.execute(
    'SELECT Album.AlbumID, Album.Title, Album.Year, Artist.Name FROM Album JOIN Artist ON Album.ArtistID = Artist.ArtistID ORDER BY Album.Title'
  ).fetchall()
  conn.close()
  return render_template('album.html', albums=albums)


@app.route('/album/songs/')
def getAlbumSongs():
  album_id = request.args.get('album_id')
  conn = get_db_connection()
  songs = conn.execute('SELECT * FROM Song WHERE AlbumID = ?',
                       (album_id, )).fetchall()
  album = conn.execute(
    'SELECT Album.Title, Album.Year, Artist.Name FROM Album JOIN Artist ON Album.ArtistID = Artist.ArtistID WHERE Album.AlbumID = ?',
    (album_id, )).fetchone()
  conn.close()
  return render_template('album_songs.html', songs=songs, album=album)


@app.route('/existing_user/new_user')
def new_user():
  return render_template('create_user.html')


@app.route('/create_user', methods=['POST'])
def create_user():
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']

  conn = get_db_connection()

  # Check if the username is already in use
  user = conn.execute('SELECT * FROM Users WHERE username = ?',
                      (username, )).fetchone()
  if user is not None:
    message = 'That username is already taken.'
    conn.close()
    return render_template('create_user.html', message=message)

  # Insert the new user into the User table
  conn.execute(
    'INSERT INTO Users (username, password, email) VALUES (?, ?, ?)',
    (username, password, email))
  conn.commit()

  # Log the user in automatically
  user = conn.execute(
    'SELECT * FROM Users WHERE username = ? AND password = ?',
    (username, password)).fetchone()
  session['user_id'] = user['UserID']

  conn.close()

  return redirect(url_for('index'))


@app.route('/existing_user')
def existing_user():
  return render_template('existing_user.html')


@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  conn = get_db_connection()

  user = conn.execute(
    'SELECT * FROM Users WHERE username = ? AND password = ?',
    (username, password)).fetchone()

  if user is None:
    message = 'Invalid username or password.'
    conn.close()
    return render_template('existing_user.html', message=message)

  # Create a session variable to store the user's UserID
  session['user_id'] = user['UserID']

  conn.close()
  return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
  session.pop('user_id', None)
  return redirect(url_for('index'))


@app.route('/genre/')
def getGenre():
  conn = get_db_connection()
  genres = conn.execute('SELECT * FROM Genre').fetchall()
  conn.close()
  return render_template('genre.html', genres=genres)


@app.route('/genre/<int:genre_id>/song')
def getSongByGenre(genre_id):
  conn = get_db_connection()
  songs = conn.execute(
    'SELECT Song.*, Artist.Name AS ArtistName, Album.Title AS AlbumTitle FROM Song JOIN Artist ON Song.ArtistID = Artist.ArtistID JOIN Album ON Song.AlbumID = Album.AlbumID JOIN SongGenre ON Song.SongID = SongGenre.SongID WHERE SongGenre.GenreID = ?',
    (genre_id, )).fetchall()
  conn.close()
  return render_template('songs.html', songs=songs)


@app.route('/search')
def search():
  genre_id = request.args.get('genre')
  if genre_id:
    conn = get_db_connection()
    genre = conn.execute('SELECT * FROM Genre WHERE GenreID = ?',
                         (genre_id, )).fetchone()
    conn.close()
    return render_template('genre.html', genres=[genre])
  else:
    return redirect('/genre/')


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0', debug=True, port=8080)
