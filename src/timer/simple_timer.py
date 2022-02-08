import sys

from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QSpinBox, QVBoxLayout, \
    QSizePolicy

from src.timer.base_timer import BaseTimer


class SimpleTimer(QWidget, BaseTimer):

    paused = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.update_timer = QTimer(self)
        self.setting_time = 0
        self.remaining = 0

        self.remain_label = QLabel('00:00', self)
        self.remain_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.remain_label.setScaledContents(True)
        font = QFont()
        font.setPointSize(86)
        self.remain_label.setFont(font)
        self.timer_edit = QSpinBox(self)
        self.timer_edit.setRange(1, 99)
        self.timer_edit.setValue(25)

        self.set_ui()
        self.set_connection()

        self.show()

    def set_ui(self):
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.remain_label, alignment=Qt.AlignHCenter)
        vlayout.addWidget(self.timer_edit)
        self.setLayout(vlayout)

    def set_connection(self):
        self.timer.timeout.connect(self.stop)
        self.update_timer.timeout.connect(self.remain_update)

    def start(self):
        self.setting_time = self.timer_edit.value()
        self.timer.start(self.setting_time * 60 * 1000)
        self.set_remain_update()
        self.started.emit()

    def set_remain_update(self):
        self.remain_update()
        self.update_timer.start(250)

    def stop(self):
        self.reset()
        self.timeout.emit()

    def abort(self):
        self.reset()
        self.timer.stop()
        self.aborted.emit()

    def pause(self):
        self.update_timer.stop()
        self.remaining = self.timer.remainingTime()
        self.timer.stop()
        self.paused.emit()

    def resume(self):
        self.timer.start(self.remaining)
        self.set_remain_update()
        self.started.emit()

    def reset(self):
        self.timer.stop()
        self.update_timer.stop()
        self.remain_label.setText('00:00')
        self.remaining = 0

    def get_notify_message(self):
        remaining = self.timer.remainingTime() / 1000
        return '{0} minutes have passed.'.format(self.setting_time - int(remaining/60))

    def remain_update(self):
        remaining = self.timer.remainingTime() / 1000
        self.remain_label.setText('{min:02}:{sec:02}'.format(
            min=int(remaining / 60), sec=int(remaining % 60)))

    @property
    def name(self):
        return 'Simple Timer'


if __name__ == '__main__':
    app = QApplication(sys.argv)

    simpleTimer = SimpleTimer()
    simpleTimer.start()
    sys.exit(app.exec_())
