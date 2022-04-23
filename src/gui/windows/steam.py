from PySide6 import QtWidgets, QtGui, QtCore
from qasync import asyncSlot
from functools import partial
from asyncio import gather
from random import choice

from . import Window

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

    @asyncSlot()
    async def return_pressed(self, line_edit):
        self.loggedin.emit(line_edit.text())
        self.close()


class SteamGameScene(QtWidgets.QGraphicsScene):
    class GamePanel(QtWidgets.QLabel):
        def __init__(self, scene, game):
            super().__init__()

            self._game = game
            self._scene = scene
            self._set_game()

            self.setMouseTracking(True)
            self.installEventFilter(self)

        def _set_game(self):
            if self._game.img:
                self.pixmap = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(self._game.img, self._game.img_type)).\
                    scaled(160, 90)
                self.setPixmap(self.pixmap)
                self.setFixedSize(QtCore.QSize(160, 90))

            else:
                self.setText(self._game.name)

        def eventFilter(self, source, event: QtCore.QEvent):
            if event.type() == QtCore.QEvent.MouseMove:
                print('hover', self._game.name)
                self._scene.set_hover(self)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                print('click', self._game.name)

            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                print('dbl click', self._game.name)

            return super().eventFilter(source, event)

        def unhover(self):
            print('unhover', self._game.name)

    class SteamGameGrid(QtWidgets.QGraphicsWidget):
        def __init__(self, scene):
            super().__init__()

            self._scene = scene

            self.setLayout(QtWidgets.QGraphicsGridLayout())
            self.games_panels = []

        def create_game_panels(self, scene, games):
            for col, game_group in enumerate([games[i:i + 4] for i in range(0, len(games), 4)]):
                self.games_panels.append(list())

                for row, game in enumerate(game_group):
                    panel = scene.addWidget(SteamGameScene.GamePanel(self._scene, game))

                    self.games_panels[col].append(panel)
                    self.layout().addItem(panel, col, row)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._view = QtWidgets.QGraphicsView(self, parent)
        self._layout = self.SteamGameGrid(self)

        self.installEventFilter(self)
        self.addItem(self._layout)
        self._hovered_game = None

    def set_hover(self, game):
        if self._hovered_game:
            self._hovered_game.unhover()

        self._hovered_game = game

    def eventFilter(self, source, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            if self._hovered_game and not self._hovered_game.underMouse():
                self._hovered_game.unhover()
                self._hovered_game = None

        return super().eventFilter(source, event)

    def set_games(self, handler, games):
        self._layout.create_game_panels(self, games)

    def add_scene_to_layout(self, layout):
        layout.addWidget(self._view)


class SteamWindow(Window):
    def __init__(self, main_window, handler):
        super(SteamWindow, self).__init__()
        self._main_window = main_window
        self._handler_cls = handler

        self.scene = SteamGameScene(parent=self)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.scene.add_scene_to_layout(self.layout)

        self.setMouseTracking(True)

        self.popup = LoginPopUp()
        self.popup.setGeometry(100, 100, 400, 200)
        self.popup.loggedin.connect(self._receive_games)
        self.popup.show()

    @asyncSlot()
    async def _receive_games(self, text):
        handler = await self._handler_cls(text)
        games = await gather(*handler.get_games())

        self.scene.set_games(handler, games)

        self._main_window.setCentralWidget(self)