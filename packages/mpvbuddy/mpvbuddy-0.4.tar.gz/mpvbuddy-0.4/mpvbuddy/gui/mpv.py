import mpv
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MPVWindow(QMainWindow):

    def __init__(self, controller):
        super().__init__(None)

        self.controller = controller
        self.controller.mpv_window = self

        # Disable close/max/min controls
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        # Attributes needed specifically for python-mpv
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.player = mpv.MPV(wid=str(int(self.container.winId())),
                              # vo='x11', # You may not need this
                              log_handler=print,
                              loglevel='info',
                              input_default_bindings=False,
                              input_vo_keyboard=False)
        self.player.observe_property('time-pos', self.time_observer)
        self.player.observe_property('fullscreen', self.fullscreen_observer)
        self.player.observe_property('pause', lambda x, y: self.controller.player_state(x, y))
        self.player.observe_property('start', lambda x, y: self.controller.player_state(x, y))
        self.player.observe_property('eof-reached', lambda x, y: self.controller.player_state(x, y))
        self.player.register_key_binding('WHEEL_UP', 'osd-msg-bar add volume 2')
        self.player.register_key_binding('WHEEL_DOWN', 'osd-msg-bar add volume -2')
        self.player.register_key_binding('MBTN9', 'seek 10')
        self.player.register_key_binding('MBTN10', 'seek -10')
        self.player.register_key_binding('MBTN_MID', 'show-progress')
        self.player.register_key_binding('MBTN_LEFT_DBL', 'cycle fullscreen')
        self.player.register_key_binding('MBTN_RIGHT', 'osd-msg-bar cycle pause')
        self.player.register_key_binding('MBTN_BACK', 'script-message extpl-back')
        self.player.register_key_binding('MBTN_FORWARD', 'script-message extpl-forward')
        self.player.register_message_handler('extpl-back', self.controller.playlist_down)
        self.player.register_message_handler('extpl-forward', self.controller.playlist_up)

    def closeEvent(self, event: QCloseEvent):
        # Don't allow this window to close on its own
        # We can't just reshow it on play; it won't be ready
        # unless we wait for the paint event and mpv will crash.
        event.ignore()

    def play(self, video_file, seek):
        self.player.play(video_file)
        self.player.wait_for_property('seekable')
        self.player.seek(seek, reference='absolute', precision='exact')

    def stop(self):
        self.player.command('stop')

    def run_seek_cmd(self, *cmd):
        try:
            self.player.command(*cmd)
        except SystemError as e:
            # There's no real way to check if we can seek and if we can't
            # we get a system error.
            self.controller.log.warn(f'Seek Error {e}')

    # This might be needed once I test on Win/Mac if I get
    # window decoration issues
    # def showFullScreen(self):
    #     # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
    #     super().showFullScreen()
    #
    # def showNormal(self):
    #     super().showNormal()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.windowState() == Qt.WindowFullScreen:
                self.showNormal()
                self.player['fullscreen'] = 'no'
            else:
                self.showFullScreen()
                self.player['fullscreen'] = 'yes'

    def mousePressEvent(self, event):
        if event.button() == Qt.BackButton:
            self.controller.playlist_down()
        elif event.button() == Qt.ForwardButton:
            self.controller.playlist_up()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Space:
            self.player.command('osd-msg-bar', 'cycle', 'pause')
        elif key == Qt.Key_Up:
            self.run_seek_cmd('osd-msg-bar', 'seek', '+30', 'relative+keyframes')
        elif key == Qt.Key_Down:
            self.run_seek_cmd('osd-msg-bar', 'seek', '-30', 'relative+keyframes')
        elif key == Qt.Key_Left:
            self.run_seek_cmd('osd-msg-bar', 'seek', '-5', 'relative+keyframes')
        elif key == Qt.Key_Right:
            self.run_seek_cmd('osd-msg-bar', 'seek', '+5', 'relative+keyframes')

    def fullscreen_observer(self, _name, value):
        if value:
            self.showFullScreen()
        else:
            self.showNormal()

    def time_observer(self, name, value):
        # Here, _value is either None if nothing is playing or a float containing
        # fractional seconds since the beginning of the file.
        if value is not None:
            self.controller.time_step(value)
