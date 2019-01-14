import sys

from PySide2.QtCore import QTimer, QTime, Signal, Qt, SLOT
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QTimeEdit, QApplication, QSpinBox, QHBoxLayout, QVBoxLayout, \
    QSizePolicy


class SimpleTimer(QWidget):

    def __init__(self, parent=None):
        start = Signal()
        finished = Signal()

        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.update_timer = QTimer(self)

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
        self.timer.start(self.timer_edit.value() * 60 * 1000)
        self.remain_update()
        self.update_timer.start(1000)

    def stop(self):
        self.timer.stop()
        self.update_timer.stop()
        self.finished.emit()

    def remain_update(self):
        remaining = self.timer.remainingTime() / 1000
        self.remain_label.setText('{min:02}:{sec:02}'.format(
            min=int(remaining / 60), sec=int(remaining % 60)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    simpleTimer = SimpleTimer()
    simpleTimer.start()
    sys.exit(app.exec_())
