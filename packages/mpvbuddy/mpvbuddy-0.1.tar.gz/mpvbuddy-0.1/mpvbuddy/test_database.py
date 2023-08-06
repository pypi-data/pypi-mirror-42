#!/usr/bin/env python3
# Author: Sumit Khanna<sumit@penguindreams.org>
# https://penguindreams.org
# Copyright 2018
#
# License: GNU GPLv3
import unittest
import tempfile
from mpvbuddy.database import Database
import sqlite3
import os


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.sqltemp = tempfile.mkstemp(suffix='.sql')
        self.db = Database(self.sqltemp[1])

    def tearDown(self):
        os.unlink(self.sqltemp[1])

    def test_default_playlist(self):
        playlists = self.db.playlists()
        self.assertTrue(len(playlists) == 1)
        self.assertTrue(playlists[0]['name'] == 'Default Playlist')

    def test_empty_playlist(self):
        self.assertTrue(len(self.db.files_for_playlist(1)) == 0)

    def test_add_file(self):
        file_url = 'file:///tmp/test.mp4'
        insert_id = self.db.add_file(1, file_url)
        inserted_model = self.db.get_file(insert_id)
        self.assertTrue(inserted_model['id'] == insert_id)
        self.assertTrue(inserted_model['playlist_id'] == 1)
        self.assertTrue(inserted_model['playtime'] == 0)
        self.assertTrue(inserted_model['finished'] == 0)
        self.assertTrue(inserted_model['url'] == file_url)

    def test_add_playlist(self):
        self.db.add_playlist('New Playlist2')
        playlists = self.db.playlists()
        self.assertTrue(len(playlists) == 2)
        self.assertIn({'id': 1, 'ordering': 1.0, 'name': 'Default Playlist'}, playlists)
        self.assertIn({'id': 2, 'ordering': 2.0, 'name': 'New Playlist2'}, playlists)

    def test_files_per_playlist(self):
        list_id = self.db.add_playlist('Second')
        self.db.add_file(1, 'file:///default_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_2.mp4')
        list_1 = self.db.files_for_playlist(1)
        list_2 = self.db.files_for_playlist(2)
        self.assertTrue(len(list_1) == 1)
        self.assertTrue(len(list_2) == 2)
        self.assertIn({'id': 1, 'playlist_id': 1, 'ordering': 1.0,
                       'playtime': 0.0, 'finished': 0,
                       'url': 'file:///default_vid_1.mp4'}, list_1)
        self.assertIn({'id': 2, 'playlist_id': 2, 'ordering': 2.0,
                       'playtime': 0.0, 'finished': 0,
                       'url': 'file:///second_vid_1.mp4'}, list_2)
        self.assertIn({'id': 3, 'playlist_id': 2, 'ordering': 3.0,
                       'playtime': 0.0, 'finished': 0,
                       'url': 'file:///second_vid_2.mp4'}, list_2)

    def test_clear_playlist(self):
        list_id = self.db.add_playlist('Second')
        self.db.add_file(1, 'file:///default_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_2.mp4')
        self.db.clear_playlist(1)
        self.assertTrue(len(self.db.files_for_playlist(1)) == 0)
        self.assertTrue(len(self.db.files_for_playlist(2)) == 2)
        self.db.clear_playlist(2)
        self.assertTrue(len(self.db.files_for_playlist(1)) == 0)
        self.assertTrue(len(self.db.files_for_playlist(2)) == 0)

    def test_delete_playlist(self):
        list_id = self.db.add_playlist('Second')
        self.db.add_file(1, 'file:///default_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_2.mp4')
        self.db.delete_playlist(1)
        self.assertTrue(len(self.db.files_for_playlist(1)) == 0)
        self.assertNotIn({'id': 1, 'ordering': 1.0, 'name': 'Default Playlist'}, self.db.playlists())
        self.assertIn({'id': 2, 'ordering': 2.0, 'name': 'Second'}, self.db.playlists())
        self.db.delete_playlist(2)
        self.assertTrue(len(self.db.playlists()) == 0)

    def test_update_file(self):
        self.db.add_file(1, 'file:///original_1.mp4')
        list_1 = self.db.files_for_playlist(1)
        model = {'id': 1, 'playlist_id': 1, 'ordering': 1.0,
                 'playtime': 0.0, 'finished': 0,
                 'url': 'file:///original_1.mp4'}
        self.assertIn(model, list_1)
        model['ordering'] = 2.3
        model['playtime'] = 405.0
        model['finished'] = 1
        model['url'] = 'file:///different_2.mkv'
        self.db.update_file(model)
        list_updated = self.db.files_for_playlist(1)
        self.assertIn(model, list_updated)
        self.assertTrue(len(list_updated) == 1)

    def test_move_file_playlist(self):
        list_id = self.db.add_playlist('Second')
        list_id = self.db.add_playlist('Third')
        id_1_1 = self.db.add_file(1, 'file:///first_1.mp4')
        id_1_2 = self.db.add_file(1, 'file:///first_2.mp4')
        id_2 = self.db.add_file(2, 'file:///second.mp4')
        id_3_1 = self.db.add_file(3, 'file:///third_1.mp4')
        id_3_2 = self.db.add_file(3, 'file:///third_2.mp4')
        id_3_3 = self.db.add_file(3, 'file:///third_3.mp4')

        move_2 = self.db.get_file(id_2)
        move_2['playlist_id'] = 3
        self.db.update_file(move_2)

        self.assertTrue(len(self.db.files_for_playlist(2)) == 0)
        self.assertTrue(len(self.db.files_for_playlist(3)) == 4)

        move_3_3 = self.db.get_file(id_3_3)
        move_3_3['playlist_id'] = 1
        self.db.update_file(move_3_3)

        self.assertTrue(len(self.db.files_for_playlist(1)) == 3)
        self.assertTrue(len(self.db.files_for_playlist(2)) == 0)
        self.assertTrue(len(self.db.files_for_playlist(3)) == 3)

    def test_remove_file(self):
        list_id = self.db.add_playlist('Foo')
        id_1 = self.db.add_file(1, 'file:///first.mp4')
        id_2 = self.db.add_file(2, 'file:///second.mp4')
        self.db.remove_file(id_2)
        self.assertTrue(len(self.db.files_for_playlist(1)) == 1)
        self.assertTrue(len(self.db.files_for_playlist(2)) == 0)
        self.db.remove_file(id_1)
        self.assertTrue(len(self.db.files_for_playlist(1)) == 0)
        self.assertTrue(len(self.db.files_for_playlist(2)) == 0)

    def test_duplicate_url(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add_file(1, 'file:///first.mp4')
            self.db.add_file(1, 'file:///first.mp4')

    def test_allow_duplicate_urls_second_playlist(self):
        self.db.add_file(1, 'file:///second.mp4')
        self.db.add_file(2, 'file:///second.mp4')
        self.assertTrue(len(self.db.files_for_playlist(1)) == 1)
        self.assertTrue(len(self.db.files_for_playlist(2)) == 1)
