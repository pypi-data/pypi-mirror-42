from yoyo import read_migrations
from yoyo import get_backend
import sqlite3
from os import path
from threading import Lock


class Database(object):

    def __init__(self, db_file):
        self.db_file = db_file
        self.migrate_schema()
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.sql_lock = Lock()

    def run_query(self, sql, args=[]):
        self.sql_lock.acquire()
        cursor = self.conn.cursor()
        result = cursor.execute(sql, args)
        self.conn.commit()
        self.sql_lock.release()
        return result

    def run_insert(self, sql, args=[]):
        self.sql_lock.acquire()
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        new_id = cursor.lastrowid
        self.conn.commit()
        self.sql_lock.release()
        return new_id

    def playlists(self):
        mapped = []
        for row in self.run_query('SELECT * FROM playlists'):
            mapped.append({'id': row[0], 'ordering': row[1], 'name': row[2]})
        return mapped

    def files_for_playlist(self, playlist_id):
        mapped = []
        for row in self.run_query('SELECT * FROM files f WHERE f.playlist_id=? ORDER BY f.ordering', [playlist_id]):
            mapped.append({'id': row[0], 'playlist_id': row[1], 'ordering': row[2], 'playtime': row[3], 'finished': row[4], 'url': row[5]})
        return mapped

    def add_playlist(self, name):
        return self.run_insert("INSERT INTO playlists(id, ordering, name) " +
                               "VALUES(NULL, (SELECT IFNULL(MAX(ordering), 0) + 1 FROM playlists), ?)",
                               [name])

    def clear_playlist(self, playlist_id):
        self.run_query("DELETE FROM files WHERE files.playlist_id=?", [playlist_id])

    def delete_playlist(self, playlist_id):
        self.clear_playlist(playlist_id)
        self.run_query("DELETE FROM playlists WHERE playlists.id=?", [playlist_id])

    def add_file(self, playlist_id, url):
        return self.run_insert("INSERT INTO files(id, playlist_id, ordering, playtime, finished, url) " +
                               "VALUES(NULL, ?, (SELECT IFNULL(MAX(ordering), 0) + 1 FROM files), 0, 0, ?)",
                               [playlist_id, url])

    def get_file(self, file_id):
        mapped = []
        for row in self.run_query("SELECT * FROM files f WHERE f.id=?", [file_id]):
            mapped.append({'id': row[0], 'playlist_id': row[1], 'ordering': row[2], 'playtime': row[3], 'finished': row[4], 'url': row[5]})
        return mapped[0] if len(mapped) > 0 else None

    def update_file(self, file_model):
        self.run_query('UPDATE files SET ordering=?, playtime=?, finished=?, playlist_id=?, url=? WHERE id=?',
                       [file_model['ordering'], file_model['playtime'],
                        file_model['finished'], file_model['playlist_id'],
                        file_model['url'], file_model['id']])

    def remove_file(self, file_id):
        self.run_query('DELETE FROM files WHERE files.id=?', [file_id])

    def migrate_schema(self):
        backend = get_backend('sqlite:////{}'.format(self.db_file))
        ddl_dir = path.join(path.dirname(path.realpath(__file__)), 'ddl')
        migrations = read_migrations(ddl_dir)
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))


if __name__ == '__main__':
    pass
    # db = Database('/home/cassius/workspace/poc-mpv-buddy-py/dev.sqlite')
    #
    # # Legacy Importer
    # videos = []
    # with open('/home/hootersmcboobies/.mpvbuddy.list', 'r') as vids:
    #     for l in vids.readlines():
    #         parts = l.split('|')
    #         videos.append({'url': parts[0], 'time': parts[1]})
    # for v in videos:
    #     time = 0
    #     finished = 0
    #     if v['time'].strip() == 'F':
    #         finished = 1
    #     else:
    #         time = float(v['time'])
    #     db.run_query("INSERT INTO files(id, playlist_id, ordering, playtime, finished, url) " +
    #                "VALUES(NULL, ?, (SELECT IFNULL(MAX(ordering), 0) + 1 FROM files), ?, ?, ?)",
    #                [1, time, finished, v['url']])
