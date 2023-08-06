#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, QSettings, QStandardPaths
import sys
import os
from mpvbuddy.broker import MessageBroker
from mpvbuddy.controller import Controller
from mpvbuddy.gui import MPVWindow, PlaylistWindow, LoggingWindow
from mpvbuddy.database import Database


if __name__ == '__main__':

    QCoreApplication.setOrganizationDomain("battlepenguin.com")
    QCoreApplication.setOrganizationName("BattlePenguin")
    QCoreApplication.setApplicationName("mpvbuddy")
    settings = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())

    # TODO: somehow set this from git tag on release
    # or mark latest tag -hash-dirty?
    QCoreApplication.setApplicationVersion("0.0.1")
    app = QApplication(sys.argv)

    log_win = LoggingWindow()

    # Create or load database
    app_data = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
    log_win.info(f'Application Data Directory {app_data}')
    if not os.path.exists(app_data):
        log_win.info(f'Data directory does not exist. Creating')
        os.makedirs(app_data)
    # todo: make configurable from command line?
    db_file = os.path.join(app_data, 'playlists.sqlite')
    log_win.info(f'Database file: {db_file}')

    # This is necessary since PyQT stomps over the locale settings needed by libmpv.
    # This needs to happen after importing PyQT before creating the first mpv.MPV instance.
    import locale  # noqa
    locale.setlocale(locale.LC_NUMERIC, 'C')
    database = Database(db_file)
    msg_broker = MessageBroker(log_win)
    msg_broker.start()
    controller = Controller(app, database, msg_broker, log_win, settings)
    player = MPVWindow(controller)
    playlist = PlaylistWindow(controller)
    controller.load_window_positions()

    controller.load_default_playlist()

    player.show()
    playlist.show()

    sys.exit(app.exec_())
