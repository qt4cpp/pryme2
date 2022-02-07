import subprocess
import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit, QPushButton, QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, \
    QSystemTrayIcon, QComboBox

from timer.simple_timer import SimpleTimer
from timer.alarm_clock import AlarmClock

cmd = 'afplay -v .3 ./resource/piano.mp3'

class Pryme2(QWidget):

    notify_request = Signal(str)

    def __init__(self, parent=None):

        super(Pryme2, self).__init__(parent)

        self.timer_instances = (SimpleTimer(), AlarmClock())
        self.timer_selection = QComboBox(self)
        for t in self.timer_instances:
            self.timer_selection.addItem(t.name)
        self.timer = self.timer_instances[0]
        self.commitment_textbox = QLineEdit(self)
        self.commitment_textbox.setPlaceholderText('What do you want to commit?')
        self.commitment_textbox.setClearButtonEnabled(True)
        self.commit_done_btn = QPushButton('&Done', self)
        self.start_btn = QPushButton('&Start', self)
        self.abort_btn = QPushButton('&Abort', self)
        self.abort_btn.hide()
        self.pause_btn = QPushButton('&Pause', self)
        self.pause_btn.hide()

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
        self.vlayout.addWidget(self.timer_selection)
        self.vlayout.addWidget(self.timer)

        self.bottom_hlayout = QHBoxLayout()
        self.bottom_hlayout.addWidget(self.start_btn)
        self.bottom_hlayout.addWidget(self.abort_btn)
        self.bottom_hlayout.addWidget(self.pause_btn)

        self.vlayout.addLayout(self.bottom_hlayout)
        self.setLayout(self.vlayout)

    def set_connection(self):
        self.timer_selection.currentIndexChanged.connect(self.change_timer)
        self.connect_timer()

    def connect_timer(self):
        self.start_btn.clicked.connect(self.timer.start)
        self.abort_btn.clicked.connect(self.timer.abort)
        self.pause_btn.clicked.connect(self.timer.pause)
        self.timer.timeout.connect(self.notify)
        self.timer.started.connect(self.set_timer_active_ui)
        self.timer.aborted.connect(self.set_timer_deactive_ui)
        self.timer.timeout.connect(self.set_timer_deactive_ui)

    def disconnect_timer(self):
        self.timer.disconnect(self)
        self.start_btn.disconnect(self.timer)
        self.abort_btn.disconnect(self.timer)

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

    def set_ui_enabled(self, enable: bool):
        self.timer_selection.setEnabled(enable)
        self.commitment_textbox.setEnabled(enable)

    def set_timer_active_ui(self):
        self.activate_start_button(False)
        self.set_ui_enabled(False)

    def set_timer_deactive_ui(self):
        self.activate_start_button(True)
        self.set_ui_enabled(True)

    def activate_start_button(self, activate: bool):
        if activate:
            # active start button
            self.start_btn.show()
            self.abort_btn.hide()
            self.pause_btn.hide()
        else:
            self.abort_btn.show()
            self.pause_btn.show()
            self.start_btn.hide()

    @Slot(int)
    def change_timer(self, index):
        self.disconnect_timer()
        self.timer.hide()
        self.vlayout.replaceWidget(self.timer, self.timer_instances[index])
        self.timer = self.timer_instances[index]
        self.connect_timer()
        self.timer.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    pryme = Pryme2()
    sys.exit(app.exec_())
