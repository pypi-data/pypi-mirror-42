from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mpvbuddy.gui.popup import FileContextMenu


class PlaylistWindow(QMainWindow):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.controller.playlist = self
        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.title = 'mpvbuddy'
        self.setWindowTitle(self.title)

        # Menubar
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.controller.exit_app)
        file_menu.addAction(exit_action)
        help_menu = main_menu.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)
        aboutQt_action = QAction('About Qt', self)
        aboutQt_action.triggered.connect(self.aboutQt)
        logwin_action = QAction('Logs', self)
        logwin_action.setShortcut('Ctrl+U')
        logwin_action.setStatusTip('Debugging Logs')
        logwin_action.triggered.connect(self.show_log_window)
        help_menu.addAction(logwin_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)
        help_menu.addAction(aboutQt_action)

        # Playlist

        self.playbox = QComboBox()
        self.playbox.currentIndexChanged.connect(self.playlist_selected)
        add_playlist = QPushButton()
        add_playlist.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        add_playlist.setFixedSize(add_playlist.minimumSizeHint())
        add_playlist.setToolTip('New Playlist')
        add_playlist.clicked.connect(self.add_playlist_click)
        self.del_playlist = QPushButton()
        self.del_playlist.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.del_playlist.setFixedSize(self.del_playlist.minimumSizeHint())
        self.del_playlist.setToolTip('Delete Current Playlist')
        self.del_playlist.clicked.connect(self.del_playlist_click)

        top_box = QWidget()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.playbox)
        top_layout.addWidget(add_playlist)
        top_layout.addWidget(self.del_playlist)
        top_box.setLayout(top_layout)

        self.table = QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTreeView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().hide()
        self.table.doubleClicked.connect(self.playlist_dbl_click)

        self.setAcceptDrops(True)

        self.controller.msg_broker.playlist_shift.connect(self.playlist_shift)
        # Row reordering
        # self.table.setDragDropMode(self.table.InternalMove)
        # self.table.setDragDropOverwriteMode(False)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)

        layout = QVBoxLayout()
        layout.addWidget(top_box)
        layout.addWidget(self.table)
        self.container.setLayout(layout)

    def closeEvent(self, e):
        self.controller.exit_app(0)

    def dragEnterEvent(self, e):
        self.controller.log.info(f'Drag Enter Mime Data: {e.mimeData()}')
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = []
        for url in e.mimeData().urls():
            urls.append(url.toString())
        self.controller.add_files_to_playlist(urls)

    def resizeEvent(self, event):
        size_col_status = self.table.sizeHintForColumn(0)
        size_col_time = self.table.sizeHintForColumn(2)
        self.controller.log.debug(f'Status/Time Column size hints {size_col_status}/{size_col_time}')
        # If the list is empty, we're going to set some hopefully sane defaults
        if size_col_status == 1:
            size_col_status = 29
        if size_col_time == 1:
            size_col_time = 107
        self.table.setColumnWidth(1, self.table.width() - size_col_status - size_col_time - 80)
        QMainWindow.resizeEvent(self, event)

    def set_playbox_model(self, model):
        self.playbox.setModel(model)

    def set_playlist_model(self, model):
        self.table.setModel(model)
        self.table.resizeColumnsToContents()
        self.resizeEvent(None)

    def open_menu(self, position):
        row = self.table.selectedIndexes()[0].row()
        model = self.table.model().model_for_row(row)
        self.controller.log.debug(f'Context Menu Opened for Row {row} / Model {model}')

        cur_video = self.table.model().current_video
        cur_loaded = False
        if cur_video is not None and cur_video['id'] == model['id']:
            self.controller.log.debug('Context Menu is for currently loaded video')
            cur_loaded = True

        popup = FileContextMenu(row, model, self.controller, cur_loaded)
        popup.exec_(self.table.viewport().mapToGlobal(position))

    # comes in via the broker from mpv mouse bindings
    @pyqtSlot(str)
    def playlist_shift(self, direction):
        new_idx = self.controller.model.current_video_idx
        if new_idx is not None:
            while (direction == 'up' and new_idx >= 0) or (direction == 'down' and new_idx < self.controller.model.rowCount(None) - 1):
                new_idx = new_idx - 1 if direction == 'up' else new_idx + 1
                new_cur = self.controller.model.current_playlist[new_idx]
                if new_cur['finished'] == 1:
                    continue
                else:
                    self.table.selectRow(new_idx)
                    self.playlist_select()
                    break

    @pyqtSlot()
    def playlist_dbl_click(self):
        self.playlist_select()

    def current_playlist_model(self):
        return self.controller.playbox_model.playlists[self.playbox.currentIndex()]

    @pyqtSlot()
    def show_log_window(self):
        self.controller.log.show()

    @pyqtSlot()
    def about(self):
        QMessageBox.about(self, "About mpvbuddy", "mpvbuddy - v0.3 - Created by Sumit Khanna\n" +
                                "GNU GPLv3\nhttps://battlepenguin.com\n\n" +
                                "Direct Dependencies:\n" +
                                "jaseg/python-mpv - GNU AGPLv3\n" +
                                "yoyo-migrations - Apache\n" +
                                "SQLite - Public Domain\n" +
                                "PyQT5 - See About QT5")

    @pyqtSlot()
    def aboutQt(self):
        QMessageBox.aboutQt(self)

    # needed outside of the QT connect slot so
    # controller can forward mpv mouse commands
    # via the broker
    def playlist_select(self):
        playlist_item_id = self.table.selectedIndexes()[0].row()
        video_model = self.table.model().current_playlist[playlist_item_id]
        self.controller.play(video_model)

    @pyqtSlot()
    def playlist_selected(self):
        self.controller.log.debug(f'Playlist Combo Box Selected Event {self.current_playlist_model()}')
        self.controller.load_playlist(self.current_playlist_model()['id'])
        if len(self.controller.playbox_model.playlists) == 1:
            self.del_playlist.setEnabled(False)
        else:
            self.del_playlist.setEnabled(True)

    @pyqtSlot()
    def add_playlist_click(self):
        (text, ok) = QInputDialog.getText(self, "New Playlist", "Playlist name:", QLineEdit.Normal, "")
        if ok and text != '':
            self.controller.playlist_new(text)

    @pyqtSlot()
    def del_playlist_click(self):
        self.controller.playlist_delete(self.current_playlist_model())
