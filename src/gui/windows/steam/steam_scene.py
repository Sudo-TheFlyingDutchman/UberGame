from PySide6 import QtWidgets, QtCore, QtGui

from .hover_cover import HoverCover


class SteamGameScene(QtWidgets.QGraphicsScene):
    class GamePanel(QtWidgets.QLabel):
        def __init__(self, scene, game):
            super().__init__()

            self._game = game
            self._scene = scene
            self._cover = HoverCover(self)
            self._set_game()

            self.setMouseTracking(True)
            self.installEventFilter(self)

        def __eq__(self, other):
            return self._game != other._game

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
                self.setPixmap(self._cover)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                print('click', self._game.name)

            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                print('dbl click', self._game.name)

            return super().eventFilter(source, event)

        def unhover(self):
            self._set_game()
            print('unhover', self._game.name)

        def __hash__(self):
            return self._game.__hash__()

    class SteamGameGrid(QtWidgets.QGraphicsWidget):
        def __init__(self, scene):
            super().__init__()

            self._scene = scene

            self.setLayout(QtWidgets.QGraphicsGridLayout())
            self.games_panels = set()

        def create_game_panels(self, scene, games):
            for col, game_group in enumerate([games[i:i + 4] for i in range(0, len(games), 4)]):

                for row, game in enumerate(game_group):
                    panel = SteamGameScene.GamePanel(self._scene, game)

                    self.games_panels.update({panel})
                    self.layout().addItem(scene.addWidget(panel), col, row)

        def addItem(self, item, col, row):
            return self.layout().addItem(item, col, row)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._view = QtWidgets.QGraphicsView(self, parent)
        self._layout = self.SteamGameGrid(self)

        self.installEventFilter(self)
        self.addItem(self._layout)
        self._hovered_games = set()

    def check_hover(self):
        hovered_games = set(filter(lambda game: bool(game) and game.underMouse(), self._hovered_games))
        for game in self._hovered_games - hovered_games:
            game.unhover()

        self._hovered_games = hovered_games

    def set_hover(self, game):
        self._hovered_games.update({game})
        self.check_hover()

    def eventFilter(self, source, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            self.check_hover()

        return super().eventFilter(source, event)

    def set_games(self, handler, games):
        self._layout.create_game_panels(self, games)

    def add_scene_to_layout(self, layout):
        layout.addWidget(self._view)
