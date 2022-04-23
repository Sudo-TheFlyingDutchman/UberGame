from PySide6 import QtWidgets, QtCore, QtGui


class SteamGameScene(QtWidgets.QGraphicsScene):
    class GamePanel(QtWidgets.QLabel):
        def __init__(self, scene, game):
            super().__init__()

            self._game = game
            self._scene = scene
            self._set_game()

            self.setMouseTracking(True)
            self.installEventFilter(self)

        def __eq__(self, other):
            return self._game != other.game

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
        if self._hovered_game  and not self._hovered_game.underMouse() and game != self._hovered_game:
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
