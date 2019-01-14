import sys

from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout

from pryme2.timer import SimpleTimer


class Pryme2(QWidget):

    def __init__(self, parent=None):

        super(Pryme2, self).__init__(parent)

        self.timer = SimpleTimer(self)
        self.commitment_textbox = QLineEdit(self)
        self.commitment_textbox.setPlaceholderText('What do you want to commit?')
        self.commitment_textbox.setClearButtonEnabled(True)
        self.commit_done_btn = QPushButton('&Done', self)
        self.start_btn = QPushButton('&Start', self)

        self.set_ui()
        self.set_connection()
        self.show()

    def set_ui(self):
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.commitment_textbox)
        self.hlayout.addWidget(self.commit_done_btn)
        self.commit_group = QGroupBox('Commitment')
        self.commit_group.setLayout(self.hlayout)

        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.commit_group)
        self.vlayout.addWidget(self.timer)
        self.vlayout.addWidget(self.start_btn)
        self.setLayout(self.vlayout)

    def set_connection(self):
        self.start_btn.clicked.connect(self.timer.start)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    pryme = Pryme2()
    sys.exit(app.exec_())
