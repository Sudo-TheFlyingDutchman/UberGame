from PySide6 import QtWidgets, QtGui, QtCore


class HoverCover(QtGui.QPixmap):
    COGWHEEL_ICON = QtGui.QImage("icon\\cogwheel.png")

    def __init__(self, background_label, parent=None):
        super(HoverCover, self).__init__()

        self._background_label = background_label
        self.fromImage(self.get_hover_image())

    def get_hover_image(self) -> QtGui.QImage:
        return self.COGWHEEL_ICON.scaled(self._background_label.size(), QtCore.Qt.KeepAspectRatio)
