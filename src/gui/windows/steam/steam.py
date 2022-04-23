from PySide6 import QtWidgets
from qasync import asyncSlot
from asyncio import gather

from gui.windows import Window

from .login import LoginPopUp
from .steam_scene import SteamGameScene


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