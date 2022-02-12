"""
pomo_timer.py

pomodoro timer の機能を提供する。
デフォルトでは、25min を 1pomodoro とし、そのあと５分の short break を入れる。
それを3回行い、4回目のpomodoro 終了後に、15分のlong break に入る。

"""
from PySide6.QtCore import QTimer, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QLayout, QSizePolicy

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

        self.settings = {'1pomo': 25, 'short_break': 5, 'long_break': 15, 'long_break_after': 4}
        self.pomo_count = 0

    def set_connection(self):
        pass
        # simple_timer と break を処理する。

    def start(self):
        self.pomo_count += 1
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

    @property
    def name(self):
        return 'Pomo Timer'
