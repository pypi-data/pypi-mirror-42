from yoyo import step

steps = [
    step("""CREATE TABLE playlists(
      id INTEGER PRIMARY KEY,
      ordering REAL,
      name TEXT NOT NULL
    )""", "DROP TABLE playlists"),
    step("""CREATE TABLE files(
      id INTEGER PRIMARY KEY,
      playlist_id INTEGER,
      ordering REAL,
      playtime REAL,
      finished INTEGER,
      url TEXT UNIQUE,
      FOREIGN KEY (playlist_id) REFERENCES playlists(id)
    )""", "DROP TABLE files"),
    step("INSERT INTO playlists(id, ordering, name) VALUES(NULL, 1, 'Default Playlist')")
]
