from PySide6 import QtWidgets, QtGui, QtCore


def _load_image(name, ext="PNG"):
    with open(f'.\\icons\\{name}.{ext.lower()}', 'rb') as img:
        return QtGui.QImage.fromData(img.read(), ext)


class HoverCover(QtGui.QImage):
    COGWHEEL_ICON = _load_image('cogwheel')

    def __init__(self, background_image):
        super(HoverCover, self).__init__(background_image)

        self._image = self.COGWHEEL_ICON.scaled(self.size() / 2, QtCore.Qt.KeepAspectRatio)
        self._painter = QtGui.QPainter()

        self._painter.begin(self)
        self._painter.drawImage(self._image.width() / 2, self._image.height() / 2, self._image)
        self._painter.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationOver)
        self._painter.end()
