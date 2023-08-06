from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class FileContextMenu(QMenu):

    def __init__(self, row: int, video_model, controller, currently_loaded: bool):

        super().__init__()

        self.video_model = video_model
        self.controller = controller
        self.row = row

        if not currently_loaded:
            self.make_action(QStyle.SP_MediaPlay, self.tr("Play"), video_model['finished'] != 1, self.play)
        else:
            self.make_action(QStyle.SP_MediaStop, self.tr("Stop"), True, self.stop)

        self.addSeparator()

        self.make_action(QStyle.SP_MediaSeekBackward, self.tr("Rewind"),
                         video_model['playtime'] != 0 or video_model['finished'] == 1, self.rewind)
        self.make_action(QStyle.SP_DialogApplyButton, self.tr("Finish"), video_model['finished'] != 1, self.finish)

        self.addSeparator()

        self.make_action(QStyle.SP_FileIcon, self.tr("Move"), True, self.move_file)
        self.make_action(QStyle.SP_DialogCancelButton, self.tr("Remove"), True, self.remove)
        self.make_action(QStyle.SP_TrashIcon, self.tr("Delete"), True, self.delete)

    def make_action(self, icon, msg, enabled, callback):
        act = QAction(
            QApplication.style().standardIcon(icon),
            msg,
            self
        )
        act.setEnabled(enabled)
        act.triggered.connect(callback)
        self.addAction(act)

    @pyqtSlot()
    def play(self):
        self.controller.play(self.video_model)

    @pyqtSlot()
    def stop(self):
        self.controller.stop()

    @pyqtSlot()
    def rewind(self):
        self.controller.rewind(self.row, self.video_model)

    @pyqtSlot()
    def finish(self):
        self.controller.finish(self.row, self.video_model)

    # move() already exists in QWidget
    @pyqtSlot()
    def move_file(self):
        self.controller.move(self.row, self.video_model)

    @pyqtSlot()
    def remove(self):
        self.controller.remove(self.row, self.video_model)

    @pyqtSlot()
    def delete(self):
        self.controller.delete(self.row, self.video_model)
