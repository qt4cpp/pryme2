"""
BaseTimer

Base class for pryme2. Users inherit this class.
BaseTimer class has signals and methods that pryme2 is required.

Signals: started, timeout, aborted
Methods: start, abort, stop, get_notify_message, name

If you need pause function, you should implement pause() in your inherit class.
"""
from abc import ABCMeta, abstractmethod

from PySide6.QtCore import Signal


class BaseTimer(metaclass=ABCMeta):

    started = Signal()
    timeout = Signal()
    aborted = Signal()

    @abstractmethod
    def start(self):
        self.started.emit()

    @abstractmethod
    def stop(self):
        self.timeout.emit()

    @abstractmethod
    def abort(self):
        self.aborted.emit()

    @abstractmethod
    def get_notify_message(self):
        return 'Invalid message.'

    @property
    @abstractmethod
    def name(self):
        return 'Base Timer'
