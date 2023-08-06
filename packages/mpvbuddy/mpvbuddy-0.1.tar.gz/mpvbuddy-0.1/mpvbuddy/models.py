from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from urllib.parse import unquote

from mpvbuddy.util import filename_from_url


class PlayListComboBoxModel(QAbstractListModel):

    def __init__(self, initial_playlists, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.playlists = initial_playlists

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole:
            return self.playlists[index.row()]['name']
        else:
            return QVariant()

    def get_playlist_row(self, playlist_id):
        return next((i for (i, d) in enumerate(self.playlists) if d['id'] == playlist_id), None)

    def rowCount(self, parent):
        return len(self.playlists)

    def headerData(self, section, orientation, role):
        if orientation != Qt.Horizontal:
            return
        elif role != Qt.DisplayRole:
            return
        elif section == 0:
            return 'Playlists'
        else:
            return QVariant()


class PlayListTableModel(QAbstractTableModel):

    def __init__(self, initial_playlist, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.current_playlist = initial_playlist
        self.current_video = None
        self.current_video_idx = None
        self.current_state = None

    def _seconds_as_playclock(self, t):
        hour = int(t / 3600)
        min = int((t - hour * 3600) / 60)
        sec = int(t - (hour * 3600) - (min * 60))
        return f'{hour:02}:{min:02}:{sec:02}'

    def model_for_row(self, row_num):
        return self.current_playlist[row_num]

    def remove_row(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.current_playlist[row]
        self.endRemoveRows()
        return True

    def url_exists(self, url):
        find = next((i for (i, d) in enumerate(self.current_playlist) if unquote(d['url']) == unquote(url)), None)
        return True if find is not None else False

    # Updates for Changing to a New Current video
    #  (note, will not actually update the video model itself, like update_row)
    def update_video(self, video_model):
        prev_idx = self.current_video_idx
        self.current_video_idx = next((i for (i, d) in enumerate(self.current_playlist) if d['id'] == video_model['id']), None)
        self.current_video = video_model
        if prev_idx is not None:
            self.dataChanged.emit(self.index(prev_idx, 0), self.index(prev_idx, 2))
        self.update_current()

    # Update for a row that is not the current video
    def update_row(self, row: int, video_model):
        self.current_playlist[row] = video_model
        self.dataChanged.emit(self.index(row, 0), self.index(row, 2))

    def update_state(self, state):
        self.current_state = state
        self.update_current()

    def update_playtime(self, seconds):
        self.current_video['playtime'] = seconds
        self.update_current()

    def update_current(self):
        if self.current_video_idx is not None:
            self.dataChanged.emit(self.index(self.current_video_idx, 0), self.index(self.current_video_idx, 2))

    def rowCount(self, parent):
        return len(self.current_playlist)

    def columnCount(self, parent):
        return 3

    def headerData(self, section, orientation, role):
        if orientation != Qt.Horizontal:
            return
        elif role != Qt.DisplayRole:
            return
        elif section == 0:
            return ''
        elif section == 1:
            return 'Video'
        elif section == 2:
            return 'Time'
        else:
            return QVariant()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                if self.current_video is not None and self.current_video == self.current_playlist[index.row()]:
                    if self.current_video['finished'] == 1 or self.current_state == 'done':
                        return QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)
                    if self.current_state == 'stopped':
                        return QApplication.style().standardIcon(QStyle.SP_MediaStop)
                    elif self.current_state == 'paused':
                        return QApplication.style().standardIcon(QStyle.SP_MediaPause)
                    elif self.current_state == 'playing':
                        return QApplication.style().standardIcon(QStyle.SP_MediaPlay)
                    elif self.current_state == 'error':
                        return QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical)
                    else:
                        return QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
                elif self.current_playlist[index.row()]['finished'] == 1:
                    return QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)
                else:
                    return QApplication.style().standardIcon(QStyle.SP_MediaStop)
            else:
                return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        else:
            if index.column() == 0:
                return QVariant()
            if index.column() == 1:
                return filename_from_url(self.current_playlist[index.row()]['url'])
            elif index.column() == 2:
                if self.current_playlist[index.row()]['finished'] == 1:
                    return 'Finished'
                else:
                    return self._seconds_as_playclock(self.current_playlist[index.row()]['playtime'])
            else:
                return 'Unknown Cell'
