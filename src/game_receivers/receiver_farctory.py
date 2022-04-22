from game_receivers.game_receivers_impl import GameReceiverMap
from asyncio import gather


class ReceiverFactory:
    @classmethod
    def walk(cls):
        for name, handler_group in GameReceiverMap.items():
            for handler in handler_group:
                yield name, handler

    @classmethod
    async def get_games(cls):
        steam = await GameReceiverMap['steam'][0]('https://steamcommunity.com/id/mizvada')
        return await gather(*list(steam.get_games()))
