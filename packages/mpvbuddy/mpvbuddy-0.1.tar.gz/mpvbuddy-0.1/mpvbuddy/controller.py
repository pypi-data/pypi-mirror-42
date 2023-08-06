from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QErrorMessage, QMessageBox, QFileDialog, QWidget, QApplication, QStyle
import os
from mpvbuddy.models import PlayListTableModel, PlayListComboBoxModel
import math
from mpvbuddy.util import filename_from_url, abs_path_from_url, show_confirm_box, show_error_box

DEFAULT_WIN_HEIGHT = 800
DEFAULT_WIN_WIDTH = 830


class Controller(object):

    def __init__(self, application: QApplication, database, broker, logger, settings):

        self.playlist = None
        self.mpv_window = None
        self.database = database
        self.model = None
        self.reload_playbox()
        self.msg_broker = broker
        self.current_playlist_id = None
        self.log = logger
        self.settings = settings
        self.application = application

        self.log.info(f'Organization Name: {QCoreApplication.organizationName()}')
        self.log.info(f'Application Name: {QCoreApplication.applicationName()}')
        self.log.info(f'Settings Location: {self.settings.fileName()}')

    def load_window_positions(self):
        """Called in main after all windows are loaded in controller but not shown"""
        r_plst = self.__restore_geometry(self.playlist, 'playlist/geometry', DEFAULT_WIN_HEIGHT, DEFAULT_WIN_WIDTH)
        r_mpv = self.__restore_geometry(self.mpv_window, 'mpvwindow/geometry', DEFAULT_WIN_HEIGHT, DEFAULT_WIN_WIDTH)
        self.__restore_geometry(self.log, 'logwindow/geometry', 1000, 500)

        if not (r_mpv or r_plst):
            self.log.debug('No Window Positions Set. Centering.')
            geo = self.application.desktop().availableGeometry()
            self.log.debug(f'Desktop size: {geo.width()}x{geo.height()}')

            # We want to put the playlist and video side-by-side on first load
            geo_left = self.application.desktop().availableGeometry()
            geo_left.setWidth(geo_left.width() - DEFAULT_WIN_HEIGHT)
            geo_right = self.application.desktop().availableGeometry()
            geo_right.setWidth(geo_right.width() + DEFAULT_WIN_HEIGHT)
            self.playlist.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.playlist.size(), geo_left))
            self.mpv_window.setGeometry(QStyle.alignedRect(Qt.RightToLeft, Qt.AlignCenter, self.mpv_window.size(), geo_right))

    def __restore_geometry(self, widget: QWidget, name: str,
                           default_width: int, default_height: int):
        geometry = self.settings.value(name)
        if geometry is None:
            self.log.debug(f'{name} has no saved position. Using default {default_width}x{default_height}')
            widget.setMinimumSize(default_width, default_height)
            return False
        else:
            self.log.debug('Restoring Log Window Size/State')
            widget.restoreGeometry(geometry)
            return True

    def exit_app(self, code=0):
        self.settings.setValue('mpvwindow/geometry', self.mpv_window.saveGeometry())
        self.settings.setValue('logwindow/geometry', self.log.saveGeometry())
        self.settings.setValue('playlist/geometry', self.playlist.saveGeometry())
        self.settings.sync()
        self.application.exit(code)

    def reload_playbox(self):
        all_playlists = self.database.playlists()
        self.playbox_model = PlayListComboBoxModel(all_playlists)
        # if len(all_playlists) <= 1:
        #     self.playlist.del_playlist.setEnabled(False)
        # else:
        #     self.playlist.del_playlist.setEnabled(True)

    def playlist_up(self):
        self.msg_broker.send(('pls-shift', 'up'))

    def playlist_down(self):
        self.msg_broker.send(('pls-shift', 'down'))

    def playlist_new(self, name):
        new_playlist_id = self.database.add_playlist(name)
        self.log.info(f'Created Playlist {name} with ID {new_playlist_id}')
        self.reload_playbox()
        combo_box_row = self.playbox_model.get_playlist_row(new_playlist_id)
        self.log.debug(f'Setting combo box row to {combo_box_row}')
        self.playlist.playbox.setCurrentIndex(combo_box_row)
        self.load_playlist(new_playlist_id)

    def playlist_delete(self, playlist_model):
        ret = show_confirm_box(self.mpv_window, 'Confirm Delete Playlist',
                               "Are you sure you want to delete {}".format(playlist_model['name']))
        if ret == QMessageBox.Ok:
            self.log.info(f'Deleting Playlist {playlist_model["id"]}')
            self.database.delete_playlist(playlist_model['id'])

            # Fixme: This should move us up one playlist, but somehow
            # we get a second combo event that loads the first playlist
            old_row = self.playbox_model.get_playlist_row(playlist_model['id'])
            new_row = old_row - 1 if old_row > 0 else 1
            new_playlist_id = self.playbox_model.playlists[new_row]['id']
            self.log.debug(f'New Playlist ID to Load: {new_playlist_id}')

            self.reload_playbox()
            self.load_playlist(new_playlist_id)

    def load_default_playlist(self):
        # TODO: restore previous playlist if it exists, else top one
        self.log.info('Loading Default Playlist')
        self.load_playlist(self.database.playlists()[0]['id'])

    def load_playlist(self, playlist_id):
        if self.current_playlist_id != playlist_id:
            self.log.info(f'Loading Playlist {playlist_id}')
            self.current_playlist_id = playlist_id
            self.model = PlayListTableModel(self.database.files_for_playlist(playlist_id))
            self.playlist.set_playbox_model(self.playbox_model)
            self.playlist.set_playlist_model(self.model)
            self.mpv_window.stop()

    def time_step(self, time):
        s = math.floor(time)
        if self.model.current_video['playtime'] != s:
            self.model.update_playtime(s)
            self.database.update_file(self.model.current_video)

    def add_files_to_playlist(self, file_urls):
        error_dialog = QErrorMessage(self.mpv_window)
        error_dialog.setModal(True)
        error_dialog.setWindowTitle('Duplicate entry error')
        new_file_models = []
        for url in file_urls:
            if self.model.url_exists(url):
                error_dialog.showMessage('File already in playlist')
            else:
                file_id = self.database.add_file(self.current_playlist_id, url)
                new_file_models.append(self.database.get_file(file_id))
        if len(new_file_models) > 0:
            for n in new_file_models:
                self.model.current_playlist.append(n)
            self.model.layoutChanged.emit()

    def player_state(self, name, val):
        if self.model is not None and self.model.current_video is not None:
            if name == 'pause':
                self.model.update_state('paused' if val else 'playing')
            elif name == 'start':
                self.model.update_state('playing')
            elif name == 'eof-reached':
                if val is False:
                    self.model.update_state('playing')
                    self.model.current_video['finished'] = 0
                elif val is None:
                    self.model.update_state('done')
                    self.model.current_video['finished'] = 1
                self.database.update_file(self.model.current_video)
            else:
                self.log.warn('Unknown player_state {} / val {}'.format(name, val))

    def is_current_video(self, video_model):
        cur_video = self.model.current_video
        if cur_video is not None:
            if cur_video['id'] == video_model['id']:
                return True
        return False

    def play(self, video_model):
        if video_model['finished'] != 1:
            self.model.update_video(video_model)
            self.model.update_state('playing')
            self.mpv_window.play(video_model['url'], video_model['playtime'])

    def stop(self):
        self.model.current_video = None
        self.mpv_window.stop()

    def remove(self, row: int, video_model):
        if self.is_current_video(video_model):
            self.stop()
        self.database.remove_file(video_model['id'])
        self.model.remove_row(row)

    def rewind(self, row: int, video_model):
        video_model['finished'] = 0
        video_model['playtime'] = 0
        self.database.update_file(video_model)
        if self.is_current_video(video_model):
            self.mpv_window.run_seek_cmd('osd-msg-bar', 'seek', '0', 'absolute')
            self.model.update_video(video_model)
        else:
            self.model.update_row(row, video_model)

    def finish(self, row: int, video_model):
        video_model['finished'] = 1
        self.database.update_file(video_model)
        if self.is_current_video(video_model):
            self.stop()
            self.model.update_video(video_model)
            self.model.current_video = None
        else:
            self.model.update_row(row, video_model)

    def move(self, row: int, video_model):

        old_path = abs_path_from_url(video_model['url'])
        file_name = os.path.basename(old_path)
        dest_dir = QFileDialog.getExistingDirectory(self.mpv_window, f"Move file {file_name}")

        if dest_dir is not '':

            new_abs_path = os.path.join(dest_dir, file_name)
            if os.path.isfile(new_abs_path):
                self.log.info(f'Destination file {new_abs_path} exists')
                ret = show_confirm_box(self.mpv_window, 'Overwrite existing file',
                                       f"{file_name} already exists in {dest_dir}. Overwrite existing file?",
                                       QMessageBox.Warning)
                if ret != QMessageBox.Ok:
                    self.log.info('Overwrite of destination file canceled')
                    return
            try:
                self.log.info(f'Moving {old_path} to {new_abs_path}')
                os.renames(old_path, new_abs_path)
                self.remove(row, video_model)
            except OSError as e:
                msg = f"Error moving {file_name} to {dest_dir}: {e.strerror}"
                self.log.error(msg)
                show_error_box(self.mpv_window, 'Error moving file', msg)
        else:
            self.log.debug(f'Canceled Move for {old_path}')

    def delete(self, row: int, video_model):
        ret = show_confirm_box(self.mpv_window, 'Confirm Delete File',
                               "Are you sure you want to delete {}".format(filename_from_url(video_model['url'])),
                               QMessageBox.Question)
        if ret == QMessageBox.Ok:
            abs_path = abs_path_from_url(video_model['url'])
            self.log.info(f'Deleting File {abs_path}')
            try:
                os.remove(abs_path)
                self.database.remove_file(video_model['id'])
                self.remove(row, video_model)
            except OSError as e:
                msg = f"Delete Error: {e.strerror}. File: {abs_path}"
                self.log.error(msg)
                show_error_box(self.mpv_window, 'Error deleting file', msg)
