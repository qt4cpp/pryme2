"""
pomo_timer.py

pomodoro timer の機能を提供する。
デフォルトでは、25min を 1pomodoro とし、そのあと５分の short break を入れる。
それを3回行い、4回目のpomodoro 終了後に、15分のlong break に入る。

"""
from PySide6.QtCore import QTimer, Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QLayout


class PomoTimer(QWidget):
    """
    PomoTimer: Pomodoro タイマーを提供する。

    1 pomodoro: 25min
    short break: 5min
    long break: 15min
    """
