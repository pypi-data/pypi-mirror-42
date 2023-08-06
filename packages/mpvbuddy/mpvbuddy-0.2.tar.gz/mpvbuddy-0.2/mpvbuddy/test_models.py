#!/usr/bin/env python3
# Author: Sumit Khanna<sumit@penguindreams.org>
# https://penguindreams.org
# Copyright 2018
#
# License: GNU GPLv3
import os
import unittest
import tempfile
from mpvbuddy.database import Database
from mpvbuddy.models import PlayListTableModel, PlayListComboBoxModel
from PyQt5.QtCore import *


class MockIndex(object):

    def __init__(self, valid, row, column):
        self.v = valid
        self.r = row
        self.c = column

    def isValid(self):
        return self.v

    def row(self):
        return self.r

    def column(self):
        return self.c


class PlayListComboBoxModelTest(unittest.TestCase):

    def setUp(self):
        self.sqltemp = tempfile.mkstemp(suffix='.sql')
        self.db = Database(self.sqltemp[1])
        self.model = PlayListComboBoxModel(self.db.playlists())

    def tearDown(self):
        os.unlink(self.sqltemp[1])

    def test_data(self):
        self.db.add_playlist('Other')
        self.model = PlayListComboBoxModel(self.db.playlists())
        self.assertTrue(self.model.data(MockIndex(False, 0, 0), Qt.DisplayRole) == None)  # noqa
        self.assertTrue(self.model.data(MockIndex(True, 0, 0), Qt.DecorationRole) == None)  # noqa
        self.assertTrue(self.model.data(MockIndex(True, 0, 0), Qt.DisplayRole) == 'Default Playlist')
        self.assertTrue(self.model.data(MockIndex(True, 1, 0), Qt.DisplayRole) == 'Other')

    def test_get_playlist_row(self):
        foo_id = self.db.add_playlist('Foo')
        bar_id = self.db.add_playlist('Bar')
        self.model = PlayListComboBoxModel(self.db.playlists())
        self.assertTrue(self.model.get_playlist_row(foo_id) == 1)
        self.assertTrue(self.model.get_playlist_row(bar_id) == 2)

    def test_row_count(self):
        self.assertTrue(self.model.rowCount(None) == 1)
        self.db.add_playlist('X')
        self.model = PlayListComboBoxModel(self.db.playlists())
        self.assertTrue(self.model.rowCount(None) == 2)
        y_id = self.db.add_playlist('Y')
        self.model = PlayListComboBoxModel(self.db.playlists())
        self.assertTrue(self.model.rowCount(None) == 3)
        self.db.delete_playlist(y_id)
        self.model = PlayListComboBoxModel(self.db.playlists())
        self.assertTrue(self.model.rowCount(None) == 2)

    def test_header_data(self):
        self.assertTrue(self.model.headerData(0, Qt.Horizontal, Qt.DisplayRole) == 'Playlists')
        self.assertTrue(self.model.headerData(1, Qt.Horizontal, Qt.DisplayRole) == None)  # noqa
        self.assertTrue(self.model.headerData(0, Qt.Vertical, Qt.DecorationRole) == None)  # noqa


class PlayListTableModelTest(unittest.TestCase):

    def setUp(self):
        self.sqltemp = tempfile.mkstemp(suffix='.sql')
        self.db = Database(self.sqltemp[1])
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.data_changes = []

    def tearDown(self):
        os.unlink(self.sqltemp[1])

    # Emitted event callbacks

    def change_event_callback(self, x, y):
        # test should reset these after each check
        self.data_changes.append({'start': x, 'end': y})

    def remove_event_callback(self, parent, first, last):
        self.data_changes.append({'first': first, 'last': last, 'parent': parent})

    # End callbacks

    def test_seconds_as_playclock(self):
        self.assertTrue(self.model._seconds_as_playclock(59) == '00:00:59')
        self.assertTrue(self.model._seconds_as_playclock(62) == '00:01:02')
        self.assertTrue(self.model._seconds_as_playclock(100) == '00:01:40')
        self.assertTrue(self.model._seconds_as_playclock(1000) == '00:16:40')
        self.assertTrue(self.model._seconds_as_playclock(10000) == '02:46:40')

    def test_model_for_row(self):
        self.db.add_file(1, 'file:///a.mp4')
        self.db.add_file(2, 'file:///2a.mp4')
        self.db.add_file(1, 'file:///b.mp4')
        self.db.add_file(1, 'file:///c.mp4')
        model_1 = PlayListTableModel(self.db.files_for_playlist(1))
        model_2 = PlayListTableModel(self.db.files_for_playlist(2))
        self.assertEqual(model_1.model_for_row(0), {'id': 1, 'playlist_id': 1, 'ordering': 1.0,
                                                    'playtime': 0.0, 'finished': 0, 'url': 'file:///a.mp4'})
        self.assertEqual(model_1.model_for_row(1), {'id': 3, 'playlist_id': 1, 'ordering': 3.0,
                                                    'playtime': 0.0, 'finished': 0, 'url': 'file:///b.mp4'})
        self.assertEqual(model_1.model_for_row(2), {'id': 4, 'playlist_id': 1, 'ordering': 4.0,
                                                    'playtime': 0.0, 'finished': 0, 'url': 'file:///c.mp4'})
        self.assertEqual(model_2.model_for_row(0), {'id': 2, 'playlist_id': 2, 'ordering': 2.0,
                                                    'playtime': 0.0, 'finished': 0, 'url': 'file:///2a.mp4'})

    def test_remove_row(self):
        self.db.add_file(1, 'file:///remove3.mkv')
        self.db.add_file(1, 'file:///remove1.mkv')
        self.db.add_file(1, 'file:///remove2.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.model.rowsAboutToBeRemoved.connect(self.remove_event_callback)

        # Remove 2
        self.model.remove_row(2)
        self.assertEqual(len(self.data_changes), 1)
        self.assertEqual(self.data_changes[0]['first'], 2)
        self.assertEqual(self.data_changes[0]['last'], 2)
        self.assertEqual(len(self.model.current_playlist), 2)
        self.data_changes = []

        # Remove 1
        self.model.remove_row(1)
        self.assertEqual(len(self.data_changes), 1)
        self.assertEqual(self.data_changes[0]['first'], 1)
        self.assertEqual(self.data_changes[0]['last'], 1)
        self.assertEqual(len(self.model.current_playlist), 1)
        self.data_changes = []

        # Remove final row
        self.model.remove_row(0)
        self.assertEqual(len(self.data_changes), 1)
        self.assertEqual(self.data_changes[0]['first'], 0)
        self.assertEqual(self.data_changes[0]['last'], 0)
        self.assertEqual(len(self.model.current_playlist), 0)
        self.data_changes = []

    def test_url_exists(self):
        self.assertFalse(self.model.url_exists('file:///foo.mkv'))
        self.db.add_file(1, 'file:///foo.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.assertTrue(self.model.url_exists('file:///foo.mkv'))

    def test_match_differnt_url_encodings(self):
        self.assertFalse(self.model.url_exists('file:///Foo Boo Cue.mkv'))
        self.assertFalse(self.model.url_exists('file:///Foo%20Boo%20Cue.mkv'))
        self.db.add_file(1, 'file:///Foo%20Boo%20Cue.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.assertTrue(self.model.url_exists('file:///Foo Boo Cue.mkv'))
        self.db.add_file(2, 'file:///Foo Boo Moot.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(2))
        self.assertTrue(self.model.url_exists('file:///Foo%20Boo%20Moot.mkv'))

    def test_update_video(self):
        self.db.add_file(1, 'file:///some.mkv')
        self.db.add_file(1, 'file:///current.mkv')
        self.db.add_file(1, 'file:///select.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.model.dataChanged.connect(self.change_event_callback)
        update_3 = {'id': 3, 'playlist_id': 1, 'ordering': 1.0,
                    'playtime': 35.0, 'finished': 1, 'url': 'file:///select_updated.mp4'}

        # Video without currently playing set

        self.model.update_video(update_3)
        self.assertEqual(self.model.current_video, update_3)
        self.assertEqual(len(self.data_changes), 1)
        change = self.data_changes[0]
        self.assertEqual(change['start'].row(), 2)
        self.assertEqual(change['start'].column(), 0)
        self.assertEqual(change['end'].row(), 2)
        self.assertEqual(change['end'].column(), 2)
        self.assertEqual(self.model.current_video_idx, 2)

        # Right now update_video doesn't update the current video model
        # update_row does. This is because update_video is used by the
        # controller for play/rewind/finish only for the currently
        # playing case
        self.assertNotEqual(self.model.current_playlist[self.model.current_video_idx], update_3)
        self.data_changes = []

        # Currently playing set
        update_1 = {'id': 2, 'playlist_id': 1, 'ordering': 1.0,
                    'playtime': 2.0, 'finished': 0, 'url': 'file:///cur_updated.mp4'}
        self.model.update_video(update_1)
        self.assertEqual(self.model.current_video, update_1)
        self.assertEqual(len(self.data_changes), 2)
        self.assertEqual(self.data_changes[0]['start'].row(), 2)
        self.assertEqual(self.data_changes[0]['start'].column(), 0)
        self.assertEqual(self.data_changes[0]['end'].row(), 2)
        self.assertEqual(self.data_changes[0]['end'].column(), 2)
        self.assertEqual(self.data_changes[1]['start'].row(), 1)
        self.assertEqual(self.data_changes[1]['start'].column(), 0)
        self.assertEqual(self.data_changes[1]['end'].row(), 1)
        self.assertEqual(self.data_changes[1]['end'].column(), 2)

    def test_update_row(self):
        self.db.add_file(1, 'file:///one.mkv')
        self.db.add_file(1, 'file:///two.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.model.dataChanged.connect(self.change_event_callback)
        update_1 = {'id': 1, 'playlist_id': 1, 'ordering': 1.0,
                    'playtime': 35.0, 'finished': 1, 'url': 'file:///one_updated.mp4'}

        self.model.update_row(0, update_1)
        self.assertIsNone(self.model.current_video)
        self.assertIsNone(self.model.current_video_idx)
        self.assertEqual(len(self.data_changes), 1)
        change = self.data_changes[0]
        self.assertEqual(change['start'].row(), 0)
        self.assertEqual(change['start'].column(), 0)
        self.assertEqual(change['end'].row(), 0)
        self.assertEqual(change['end'].column(), 2)
        # Opposite of update_video, the model does update here
        self.assertEqual(self.model.current_playlist[0], update_1)
        self.data_changes = []

        self.model.current_video = update_1
        self.model.current_video_idx = 99

        update_2 = {'id': 2, 'playlist_id': 1, 'ordering': 1.0,
                    'playtime': 1.0, 'finished': 0, 'url': 'file:///two_updated.mp4'}
        self.model.update_row(1, update_2)
        # These should not change
        self.assertEqual(self.model.current_video, update_1)
        self.assertEqual(self.model.current_video_idx, 99)
        self.assertEqual(len(self.data_changes), 1)
        change = self.data_changes[0]
        self.assertEqual(change['start'].row(), 1)
        self.assertEqual(change['start'].column(), 0)
        self.assertEqual(change['end'].row(), 1)
        self.assertEqual(change['end'].column(), 2)

    @unittest.skip('TODO')
    def test_update_state(self):
        pass

    @unittest.skip('TODO')
    def test_update_playtime(self):
        pass

    def test_update_current(self):
        self.db.add_file(1, 'file:///one.mkv')
        self.db.add_file(1, 'file:///two.mkv')
        self.db.add_file(1, 'file:///three.mkv')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.model.dataChanged.connect(self.change_event_callback)
        self.model.update_current()
        self.assertEqual(len(self.data_changes), 0)
        self.model.current_video_idx = 2
        self.model.update_current()
        self.assertEqual(len(self.data_changes), 1)
        change = self.data_changes[0]
        self.assertEqual(change['start'].row(), 2)
        self.assertEqual(change['start'].column(), 0)
        self.assertEqual(change['end'].row(), 2)
        self.assertEqual(change['end'].column(), 2)

    def test_playlist_row_count(self):
        self.db.add_playlist('Play List 2')
        self.db.add_playlist('Play List 3')
        self.db.add_file(1, 'file:///default_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_1.mp4')
        self.db.add_file(2, 'file:///second_vid_2.mp4')
        self.model = PlayListTableModel(self.db.files_for_playlist(1))
        self.assertTrue(self.model.rowCount(None) == 1)
        self.model = PlayListTableModel(self.db.files_for_playlist(2))
        self.assertTrue(self.model.rowCount(None) == 2)
        self.model = PlayListTableModel(self.db.files_for_playlist(3))
        self.assertTrue(self.model.rowCount(None) == 0)

    def test_column_count(self):
        self.assertTrue(self.model.columnCount(None), 3)

    @unittest.skip('TODO')
    def test_header_data(self):
        pass

    @unittest.skip('TODO')
    def test_data(self):
        pass
