import sys

from PySide6.QtWidgets import QMainWindow, QApplication


from pryme2 import Pryme2


class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.pryme = Pryme2(self)
        self.set_ui()
        self.set_connection()
        self.show()

    def set_ui(self):
        self.setCentralWidget(self.pryme)

    def set_connection(self):
        pass
 #       self.pryme.notify_request.connect(self.notify_on_tray)

    def notify_on_tray(self, title='Timeout', message='Timeout'):
        pass
#        self.tray.showMessage(title, message)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    sys.exit(app.exec_())
