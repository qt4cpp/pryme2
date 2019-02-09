import subprocess
import sys

from PySide2.QtCore import Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, \
    QSystemTrayIcon
from timer.simple_timer import SimpleTimer

cmd = 'afplay -v .3 ./resource/piano.mp3'

class Pryme2(QWidget):

    notify_request = Signal(str)

    def __init__(self, parent=None):

        super(Pryme2, self).__init__(parent)

        self.timer = SimpleTimer(self)
        self.commitment_textbox = QLineEdit(self)
        self.commitment_textbox.setPlaceholderText('What do you want to commit?')
        self.commitment_textbox.setClearButtonEnabled(True)
        self.commit_done_btn = QPushButton('&Done', self)
        self.start_btn = QPushButton('&Start', self)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('pryme-logo.svg'))
        self.tray.show()

        self.set_ui()
        self.set_connection()
        self.show()

    def set_ui(self):
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.commitment_textbox)
        self.hlayout.addWidget(self.commit_done_btn)
        self.commit_group = QGroupBox('Commitment')
        self.commit_group.setLayout(self.hlayout)

        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.commit_group)
        self.vlayout.addWidget(self.timer)
        self.vlayout.addWidget(self.start_btn)
        self.setLayout(self.vlayout)

    def set_connection(self):
        self.start_btn.clicked.connect(self.timer.start)
        self.timer.timeout.connect(self.notify)

    def notify(self):
        title = self.commitment_textbox.text()
        if not title:
            title = 'Time up!'
        message = self.timer.get_notify_message()
        if not message:
            print(message)
            message = 'Time up!'
        self.tray.showMessage(title, message)
        subprocess.Popen(cmd.split())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    pryme = Pryme2()
    sys.exit(app.exec_())
