from queue import Queue
from PyQt5.QtCore import QThread, pyqtSignal


class MessageBroker(QThread):

    playlist_shift = pyqtSignal(str)

    def __init__(self, logger):
        QThread.__init__(self)
        self.messages = Queue()
        self.log = logger

    def send(self, msg):
        self.messages.put(msg)

    def run(self):
        while True:
            msg = self.messages.get()
            if msg[0] == 'pls-shift':
                self.playlist_shift.emit(str(msg[1]))
            else:
                self.log.error(f'Unknown message in Broker: {msg}')
