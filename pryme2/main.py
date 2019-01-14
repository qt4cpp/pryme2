import sys

from PySide2.QtWidgets import QMainWindow, QApplication

from pryme2 import Pryme2


class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.pryme = Pryme2()

        self.set_ui()
        self.show()

    def set_ui(self):
        self.setCentralWidget(self.pryme)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    sys.exit(app.exec_())
