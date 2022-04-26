from PySide6 import QtWidgets, QtCore, QtGui

from gui.utils.hovarable_grid import HovarablePanel, HovarableScene

from .hover_cover import HoverCover


class SteamGameScene(HovarableScene):
    class GamePanel(HovarablePanel):
        def __init__(self, scene, game):
            super().__init__(scene)

            self._game = game
            self._image = QtGui.QImage.fromData(self._game.img, self._game.img_type).scaled(160, 90)
            self._cover = HoverCover(self._image)

        def set_default(self):
            if self._game.img:
                self.setFixedSize(QtCore.QSize(160, 90))

            else:
                self.setText(self._game.name)

            self.setPixmap(QtGui.QPixmap.fromImage(self._image))

        def set_hover(self):
            self.setPixmap(QtGui.QPixmap.fromImage(self._cover))

        def __hash__(self):
            return self._game.__hash__()

        def eventFilter(self, source, event: QtCore.QEvent):
            if event.type() == QtCore.QEvent.MouseButtonPress:
                print('click', self._game.name)

            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                print('dbl click', self._game.name)

            return super().eventFilter(source, event)

    def create_game_panels(self, games):
        for col, game_group in enumerate([games[i:i + 4] for i in range(0, len(games), 4)]):

            for row, game in enumerate(game_group):
                self.add_panel(SteamGameScene.GamePanel(self, game), col, row)

    def set_games(self, handler, games):
        self.create_game_panels(games)
