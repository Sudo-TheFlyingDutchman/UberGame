import asyncio
from functools import partial
from PySide6 import QtWidgets, QtGui, QtQml
from qasync import asyncSlot, QApplication

from game_receivers.receiver_farctory import ReceiverFactory
from .windows import WindowFactory


class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar()

        self.create_providers_menubar()

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Menubar')

        self.setStyleSheet(
        """
        QListWidget {
            color: #FFFFFF;
            background-color: #33373B;
        }
        
        QListWidget::item {
            height: 50px;
        }
        
        QListWidget::item:selected {
            background-color: #2ABf9E;
        }
        
        QLabel {
            background-color: #FFFFFF;
            qproperty-alignment: AlignCenter;
        }
        
        QPushButton {
            background-color: #2ABf9E;
            padding: 20px;
            font-size: 18px;
        }"""
        )

        self.show()

    def create_providers_menubar(self):
        providers_menu = self.addToolBar('Providers')

        for name, handler in ReceiverFactory.walk():
            icon = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(*handler.picture())))
            action = QtGui.QAction(icon, f'&{name}', self)
            action.triggered.connect(partial(self._providers_action, name, handler))
            providers_menu.addAction(action)

    @asyncSlot()
    async def _providers_action(self, name, handler):
        window = WindowFactory.create(name, self, handler)
        self.setCentralWidget(window)


async def gui_main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    engine = QtQml.QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('O:\\Computes\\PythonProjects\\UberGame\\main.qml')
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            partial(close_future, future, loop)
        )

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    await future
    return True