"""
BaseTimer

Base class for pryme2. Users inherit this class.
BaseTimer class has signals and methods that pryme2 is required.

Signals: started, timeout, aborted
Methods: start, abort, stop, get_notify_message, name

If you need pause function, you should implement pause() in your inherit class.
"""

from PySide6.QtCore import Signal


class BaseTimer():

    started = Signal()
    timeout = Signal()
    aborted = Signal()

    def start(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def abort(self):
        raise NotImplemented

    def get_notify_message(self):
        raise NotImplemented

    @property
    def name(self):
        raise NotImplemented
