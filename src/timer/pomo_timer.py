"""
pomo_timer.py

pomodoro timer の機能を提供する。
デフォルトでは、25min を 1pomodoro とし、そのあと５分の short break を入れる。
それを3回行い、4回目のpomodoro 終了後に、15分のlong break に入る。

"""
from PySide6.QtCore import QTimer, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QLayout, QSizePolicy, QSpinBox, QHBoxLayout, QVBoxLayout

from src.timer import SimpleTimer
from src.timer.base_timer import BaseTimer


class PomoTimer(QWidget, BaseTimer):
    """
    PomoTimer: Pomodoro タイマーを提供する。

    1 pomodoro: 25min
    short break: 5min
    long break: 15min
    long break after 4pomodoro.
    """

    paused = Signal()

    def __init__(self):
        super().__init__()
        self.simple_timer = SimpleTimer(self)

        self.settings = {'pomo': 25, 'short_break': 5, 'long_break': 15, 'long_break_after': 4}
        self.work_timer = QTimer(self)
        self.work_timer.setSingleShot(True)
        self.break_timer = QTimer(self)
        self.break_timer.setSingleShot(True)

        self.pomo_count = 0
        self.estimate_pomo = 0
        self.estimate_label = QLabel(self)
        self.estimate_label.setText('Estimate: ')
        self.estimate_pomo_widget = QSpinBox(self)
        self.estimate_pomo_widget.setValue(4)
        self.estimate_pomo_widget.setSuffix('  pomo')
        self.estimate_pomo_widget.setRange(1, 20)

        self.set_ui()
        self.set_connection()

    def set_ui(self):
        layout = self.simple_timer.layout()
        i = layout.indexOf(self.simple_timer.timer_edit)
        layout.takeAt(i)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.estimate_label)
        hlayout.addWidget(self.estimate_pomo_widget)

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.simple_timer)
        self.setLayout(vlayout)

    def set_connection(self):
        # self.simple_timer.timeout.connect(self.timeout)
        self.work_timer.timeout.connect(self.timeout)
        self.break_timer.timeout.connect(self.start_work)

    def start(self):
        self.estimate_pomo = self.estimate_pomo_widget.value()
        self.start_work()

    def start_work(self):
        """
        Start timer for working on the task.
        :return:
        """
        self.simple_timer.timer = self.work_timer
        self.simple_timer.timer_edit.setValue(self.settings['pomo'])
        self.simple_timer.start()
        self.started.emit()

    def start_break(self):
        """
        Start timer for working on the rest.
        Short break is normal break, long break comes every some tasks(default 4).
        :return:
        """
        self.simple_timer.timer = self.break_timer
        if self.pomo_count % self.settings['long_break_after']:
            self.simple_timer.timer_edit.setValue(self.settings['short_break'])
        else:
            self.simple_timer.timer_edit.setValue(self.settings['long_break'])
        self.simple_timer.start()
        self.started.emit()

    def abort(self):
        self.simple_timer.abort()
        self.aborted.emit()

    def pause(self):
        self.simple_timer.pause()
        self.paused.emit()

    def resume(self):
        self.simple_timer.resume()
        self.started.emit()

    def timeout(self):
        self.pomo_count += 1
        if self.pomo_count >= self.estimate_pomo:
            self.reset()
            self.finished.emit()
        else:
            self.start_break()

    def reset(self):
        self.pomo_count = 0
        self.simple_timer.reset()
        self.work_timer.stop()
        self.break_timer.stop()

    def get_notify_message(self):
        return ''

    @property
    def name(self):
        return 'Pomo Timer'

    def fake_start(self):
        self.simple_timer.setting_time = self.simple_timer.timer_edit.value()
        self.simple_timer.timer.start(self.simple_timer.setting_time * 1000)
        self.simple_timer.set_remain_update()
        self.simple_timer.started.emit()
