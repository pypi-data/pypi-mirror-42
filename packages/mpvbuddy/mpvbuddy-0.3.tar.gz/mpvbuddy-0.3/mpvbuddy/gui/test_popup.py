import unittest

from PyQt5.QtWidgets import QApplication
import sys
from mpvbuddy.gui import FileContextMenu


class MockController(object):

    def __init__(self):
        self.action = None

    def play(self, video_model):
        self.action = {'action': 'play', 'video_model': video_model}

    def stop(self):
        self.action = {'action': 'stop'}

    def rewind(self, row, video_model):
        self.action = {'action': 'rewind', 'video_model': video_model, 'row': row}

    def finish(self, row, video_model):
        self.action = {'action': 'finish', 'video_model': video_model, 'row': row}

    def move(self, row, video_model):
        self.action = {'action': 'move', 'video_model': video_model, 'row': row}

    def remove(self, row, video_model):
        self.action = {'action': 'remove', 'video_model': video_model, 'row': row}

    def delete(self, row, video_model):
        self.action = {'action': 'delete', 'video_model': video_model, 'row': row}


class PopupTest(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.controller = MockController()

    def action(self, name: str):
        for a in self.menu.actions():
            if a.text() == name:
                return a

    def test_layout(self):
        video_model = {'finished': 0, 'playtime': 0}
        menu = FileContextMenu(0, video_model, self.controller, False)
        self.assertEqual(len(menu.actions()), 8)
        for i, action in enumerate(menu.actions()):
            if i == 1 or i == 4:
                self.assertTrue(action.isSeparator())
            else:
                self.assertFalse(action.isSeparator())

    def test_current_loaded(self):
        video_model = {'finished': 0, 'playtime': 0}
        self.menu = FileContextMenu(0, video_model, self.controller, True)
        self.assertIsNone(self.action('Play'))
        self.assertTrue(self.action('Stop').isEnabled())

    def test_not_current_loaded_finished(self):
        video_model = {'finished': 1, 'playtime': 0}
        self.menu = FileContextMenu(0, video_model, self.controller, False)
        self.assertIsNotNone(self.action('Play'))
        self.assertFalse(self.action('Play').isEnabled())
        self.assertTrue(self.action('Rewind').isEnabled())
        self.assertFalse(self.action('Finish').isEnabled())

    def test_not_current_loaded_unfinished_non_zero_playtime(self):
        video_model = {'finished': 0, 'playtime': 10}
        self.menu = FileContextMenu(0, video_model, self.controller, False)
        self.assertIsNotNone(self.action('Play'))
        self.assertTrue(self.action('Play').isEnabled())
        self.assertTrue(self.action('Rewind').isEnabled())
        self.assertTrue(self.action('Finish').isEnabled())

    def test_not_current_loaded_unfinished_zero_playtime(self):
        video_model = {'finished': 0, 'playtime': 0}
        self.menu = FileContextMenu(0, video_model, self.controller, False)
        self.assertIsNotNone(self.action('Play'))
        self.assertTrue(self.action('Play').isEnabled())
        self.assertFalse(self.action('Rewind').isEnabled())
        self.assertTrue(self.action('Finish').isEnabled())

    def test_call_play(self):
        video_model = {'finished': 0, 'playtime': 44}
        self.menu = FileContextMenu(0, video_model, self.controller, False)
        self.action('Play').trigger()
        self.assertEqual(self.controller.action, {'action': 'play', 'video_model': video_model})

    def test_call_stop(self):
        video_model = {'finished': 0, 'playtime': 55}
        self.menu = FileContextMenu(0, video_model, self.controller, True)
        self.action('Stop').trigger()
        self.assertEqual(self.controller.action, {'action': 'stop'})

    def test_call_rewind(self):
        video_model = {'finished': 0, 'playtime': 66}
        self.menu = FileContextMenu(3, video_model, self.controller, False)
        self.action('Rewind').trigger()
        self.assertEqual(self.controller.action, {'action': 'rewind', 'video_model': video_model, 'row': 3})

    def test_call_finish(self):
        video_model = {'finished': 0, 'playtime': 77}
        self.menu = FileContextMenu(4, video_model, self.controller, False)
        self.action('Finish').trigger()
        self.assertEqual(self.controller.action, {'action': 'finish', 'video_model': video_model, 'row': 4})

    def test_call_move(self):
        video_model = {'finished': 0, 'playtime': 88}
        self.menu = FileContextMenu(5, video_model, self.controller, False)
        self.action('Move').trigger()
        self.assertEqual(self.controller.action, {'action': 'move', 'video_model': video_model, 'row': 5})

    def test_call_remove(self):
        video_model = {'finished': 0, 'playtime': 99}
        self.menu = FileContextMenu(6, video_model, self.controller, False)
        self.action('Remove').trigger()
        self.assertEqual(self.controller.action, {'action': 'remove', 'video_model': video_model, 'row': 6})

    def test_call_delete(self):
        video_model = {'finished': 0, 'playtime': 101}
        self.menu = FileContextMenu(7, video_model, self.controller, False)
        self.action('Delete').trigger()
        self.assertEqual(self.controller.action, {'action': 'delete', 'video_model': video_model, 'row': 7})
