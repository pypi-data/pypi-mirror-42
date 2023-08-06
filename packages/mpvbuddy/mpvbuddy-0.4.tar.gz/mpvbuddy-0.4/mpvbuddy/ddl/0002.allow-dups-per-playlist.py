from yoyo import step

steps = [
    step("""CREATE TABLE files2(
      id INTEGER PRIMARY KEY,
      playlist_id INTEGER,
      ordering REAL,
      playtime REAL,
      finished INTEGER,
      url TEXT,
      UNIQUE(playlist_id, url),
      FOREIGN KEY (playlist_id) REFERENCES playlists(id)
    )"""),
    step("""INSERT INTO files2(id, playlist_id, ordering, playtime, finished, url)
            SELECT id, playlist_id, ordering, playtime, finished, url FROM files"""),
    step("DROP TABLE files"),
    step("ALTER TABLE files2 RENAME TO files")
]
