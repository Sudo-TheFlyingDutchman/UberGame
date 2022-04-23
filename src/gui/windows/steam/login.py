from functools import partial
from PySide6 import QtWidgets, QtCore


class LoginPopUp(QtWidgets.QWidget):
    loggedin = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        line_edit = QtWidgets.QLineEdit()
        line_edit.setText('https://steamcommunity.com/id/mizvada/')
        layout.addWidget(line_edit)

        line_edit.returnPressed.connect(partial(self.return_pressed, line_edit))

    @QtCore.Slot()
    def return_pressed(self, line_edit):
        self.loggedin.emit(line_edit.text())
        self.close()
