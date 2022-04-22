from utils.module_map import ModuleMap
from PySide6 import QtWidgets

class Window(QtWidgets.QWidget):
    pass

class WindowFactory:
    class WindowMap(ModuleMap, base_class=Window, package=__package__, file=__file__):
        pass

    @classmethod
    def create(cls, name, main_window, handler) -> QtWidgets.QWidget:
        return cls.WindowMap[name][0](main_window, handler)

