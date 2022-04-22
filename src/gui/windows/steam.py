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


class GamePanel(QtWidgets.QLabel):
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            print('hover', self._game.name)

        elif event.type() == QtCore.QEvent.MouseButtonPress:
            print('click', self._game.name)

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            print('dbl click', self._game.name)

        return super(GamePanel, self).eventFilter(source, event)

    def __init__(self, parent, game):
        super(GamePanel, self).__init__()
        self._game = game

        self.setMouseTracking(True)
        self.installEventFilter(self)
        self._set_game()

    def _set_game(self):
        if self._game.img:
            self.pixmap = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(self._game.img,
                                                                                                      self._game.img_type)).\
                scaled(160, 90)
            self.setPixmap(self.pixmap)
            self.setFixedSize(QtCore.QSize(160, 90))

        else:
            self.setText(self._game.name)


class SteamGamesWindow(QtWidgets.QWidget):
    def __init__(self, handler, games):
        super(SteamGamesWindow, self).__init__()

        self._handler = handler
        self._games = games

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.games_pannels = []
        self.create_game_grid()

    def create_game_grid(self):
        self.games_pannels = []

        for col, game_group in enumerate([self._games[i:i+4] for i in range(0, len(self._games), 4)]):
            self.games_pannels.append(list())

            for row, game in enumerate(game_group):
                pannel = GamePanel(self, game)

                self.games_pannels[col].append(pannel)
                self.layout.addWidget(pannel, col, row)


class SteamWindow(Window):
    def __init__(self, main_window, handler):
        super(SteamWindow, self).__init__()
        self._main_window = main_window
        self._handler_cls = handler

        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)

        self.popup = LoginPopUp()
        self.popup.setGeometry(100, 100, 400, 200)
        self.popup.loggedin.connect(self._receive_games)
        self.popup.show()

    @asyncSlot()
    async def _receive_games(self, text):
        handler = await self._handler_cls(text)
        games = await gather(*handler.get_games())

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setGeometry(10, 10, 200, 200)

        self.current_games = SteamGamesWindow(handler, games)

        self.scroll_area.setWidget(self.current_games)
        self._main_window.setCentralWidget(self.scroll_area)

