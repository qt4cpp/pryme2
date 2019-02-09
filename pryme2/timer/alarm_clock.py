import sys

from PySide2.QtCore import QTime, Signal, QTimer
from PySide2.QtWidgets import QWidget, QTimeEdit, QPushButton, QLabel, QVBoxLayout, QApplication


class AlarmClock(QWidget):

    started = Signal()
    aborted = Signal()
    timeout = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)
        self.alarm = QTime()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(1000)

        self.current_label = QLabel('')
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat('H:mm')
        self.set_around_btn = QPushButton('Set around time', self)

        self.set_ui()
        self.set_connection()
        self.reset()

        self.update_timer.start()
        self.set_around_time()

    def set_ui(self):
        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.current_label)
        self.vlayout.addWidget(self.time_edit)
        self.vlayout.addWidget(self.set_around_btn)

    def set_connection(self):
        self.timer.timeout.connect(self.stop)
        self.update_timer.timeout.connect(self.update_label)
        self.set_around_btn.clicked.connect(self.set_around_time)

    def set_around_time(self):
        current = QTime.currentTime()
        if current.minute() < 29:
            self.time_edit.setTime(QTime(current.hour(), 30))
        else:
            self.time_edit.setTime(QTime(current.hour()+1, 0))

    def update_label(self):
        current = QTime.currentTime()
        self.current_label.setText('{hour:02}:{min:02}:{sec:02}'.format(
            hour=current.hour(), min=current.minute(), sec=current.second()))

    def start(self):
        self.alarm = self.time_edit.time()
        self.timer.start(QTime.currentTime().msecsTo(self.alarm))
        self.started.emit()

    def abort(self):
        self.reset()
        self.aborted.emit()

    def stop(self):
        self.reset()
        self.timeout.emit()

    def reset(self):
        self.timer.stop()

    def get_notify_message(self):
        return ''

    @property
    def name(self):
        return 'Alarm Clock'


if __name__ == '__main__':
    app = QApplication(sys.argv)

    AlarmClock = AlarmClock()
    AlarmClock.show()
    sys.exit(app.exec_())
