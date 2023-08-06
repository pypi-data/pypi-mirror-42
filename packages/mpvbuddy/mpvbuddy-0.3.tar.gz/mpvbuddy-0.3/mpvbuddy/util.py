from os.path import basename
from urllib.parse import unquote, urlparse
from PyQt5.QtWidgets import QMessageBox, QWidget, QErrorMessage


def filename_from_url(url):
    """Returns the base human readable filename from a file URL"""
    return unquote(basename(urlparse(url).path))


def abs_path_from_url(url):
    return unquote(urlparse(url).path)


def show_confirm_box(parent: QWidget, title: str, message: str, icon=None):
    confirm_msg = QMessageBox(parent)
    confirm_msg.setModal(True)
    confirm_msg.setWindowTitle(title)
    confirm_msg.setText(message)
    confirm_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    confirm_msg.setDefaultButton(QMessageBox.Cancel)
    if icon is not None:
        confirm_msg.setIcon(icon)
    return confirm_msg.exec()


def show_error_box(parent: QWidget, title: str, message: str):
    error_dialog = QErrorMessage(parent)
    error_dialog.setModal(True)
    error_dialog.setWindowTitle(title)
    error_dialog.showMessage(message)
