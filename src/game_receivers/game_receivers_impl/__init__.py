from utils.module_map import ModuleMap
from ..game_receiver import GameReceiverHandler, Game

class GameReceiverMap(ModuleMap, base_class=GameReceiverHandler, package=__package__, file=__file__):
    pass
