from PySide6 import QtWidgets, QtCore, QtGui

from abc import ABCMeta, abstractmethod


class HovarableMeta(type(QtWidgets.QLabel), ABCMeta):
    ...


class HovarablePanel(QtWidgets.QLabel, metaclass=HovarableMeta):
    def __init__(self, scene):
        super().__init__()

        self._scene = scene

        self.setMouseTracking(True)
        self.installEventFilter(self)

    @abstractmethod
    def __hash__(self):
        ...

    @abstractmethod
    def set_default(self):
        ...

    @abstractmethod
    def set_hover(self):
        ...

    def __eq__(self, other):
        return hash(self) == hash(other)

    def eventFilter(self, source, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.MouseMove:
            self._scene.set_hover(self)
            self.set_hover()

        elif event.type() == QtCore.QEvent.MouseButtonPress:
            pass

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            pass

        return super().eventFilter(source, event)

    def unhover(self):
        self.set_default()


class HovarableScene(QtWidgets.QGraphicsScene):
    class HovarableGrid(QtWidgets.QGraphicsWidget):
        def __init__(self, scene):
            super().__init__()

            self._scene = scene

            self.setLayout(QtWidgets.QGraphicsGridLayout())
            self.games_panels = set()

        def addItem(self, item, col, row):
            return self.layout().addItem(item, col, row)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._view = QtWidgets.QGraphicsView(self, parent)
        self._grid = self.HovarableGrid(self)

        self.panels = set()

        self.installEventFilter(self)
        self.addItem(self._grid)
        self._hovered_panel = set()

    def add_panel(self, panel: HovarablePanel, col, row):
        self.panels.update([panel])
        self._grid.addItem(self.addWidget(panel), col, row)

    def check_hover(self):
        hovered_games = set(filter(lambda game: bool(game) and game.underMouse(), self._hovered_panel))
        for game in self._hovered_panel - hovered_games:
            game.unhover()

        self._hovered_panel = hovered_games

    def set_hover(self, panel):
        self._hovered_panel.update({panel})
        self.check_hover()

    def eventFilter(self, source, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            self.check_hover()

        return super().eventFilter(source, event)

    def add_scene_to_layout(self, layout):
        layout.addWidget(self._view)
