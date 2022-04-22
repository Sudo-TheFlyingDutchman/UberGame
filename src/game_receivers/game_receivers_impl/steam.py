from pathlib import Path
from pydantic.dataclasses import dataclass
from typing import Iterable, List, Awaitable, Tuple
from dataclasses import field
from steam.steamid import SteamID, from_url
from steam.webapi import WebAPI, webapi_request
from requests.exceptions import HTTPError

from utils.cacher import Cacher
from config_loaders import ConfigsMap

from . import GameReceiverHandler, Game


@dataclass
class _Game:
    appid: int
    name: str
    playtime_forever: int
    img_icon_url: str = field(repr=False)
    playtime_windows_forever: int
    playtime_mac_forever: int
    playtime_linux_forever: int

    playtime_2weeks: int = field(default=0)
    has_community_visible_stats: bool = field(default=False)
    icon_img: bytes = field(default=None, repr=False)
    header_img: bytes = field(default=None, repr=False)
    capsule_img: bytes = field(default=None, repr=False)

    @classmethod
    def _get_picture(cls, url):
        try:
            return webapi_request(url, params={'raw_content': True})
        except HTTPError as e:
            if not e.response.status_code == 404:
                raise e from None

    @property
    def img(self):
        if self.capsule_img:
            return self.capsule_img
        elif self.header_img:
            return self.header_img
        elif self.icon_img:
            return self.icon_img

        return None

    @property
    def img_icon_full_url(self):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.img_icon_url}.jpg'

    @property
    def img_header_full_url(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/header.jpg'

    @property
    def img_capsule_full_url(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/capsule_616x353.jpg'

    def __post_init__(self):
        if self.img_icon_url:
            self.icon_img = self._get_picture(self.img_icon_full_url)

        self.header_img = self._get_picture(self.img_header_full_url)
        self.capsule_img = self._get_picture(self.img_capsule_full_url)

    async def to_game_object(self) -> Game:
        return Game(name=self.name, img=self.img, playtime=self.playtime_forever, img_type='JPG',
                    resent_playtime=(7*24*60, self.playtime_2weeks) if self.playtime_2weeks else (-1, -1))


@dataclass
class _Games:
    game_count: int
    games: List[_Game]


class SteamReceiver(GameReceiverHandler):
    @Cacher.cache_calls(Path('steam-api'), 'get_games')
    class WebApiWrapper:
        API_TOKEN: str = ConfigsMap['steam']['STEAM_API']['KEY']
        private_api: WebAPI = WebAPI(key=API_TOKEN)
        public_api: WebAPI = WebAPI(key=None)

        async def get_games(self, steam_id):
            return _Games(**self.private_api.call('IPlayerService.GetOwnedGames', steamid=steam_id,
                                                  include_appinfo=True, include_played_free_games=True,
                                                  appids_filter=[],
                                                  include_free_sub=False)['response'])

        def __repr__(self):
            return f'<SteamReceiver(public_api=WebAPI(key=None), ' \
                   f'private_api=WebAPI(key={self.API_TOKEN}))>'

    id: SteamID
    _games: _Games
    _web_api: WebApiWrapper = WebApiWrapper()

    def __init__(self, community: str):
        self.id = from_url(community)

    def __await__(self):
        self._games = yield from self._web_api.get_games(self.id).__await__()
        return self

    @classmethod
    def picture(cls) -> Tuple[bytes, str]:
        with open("./icons/steam.jpg", "rb") as f:
            return f.read(), "JPG"

    def receive(self) -> Iterable[Awaitable[Game]]:
        return [game.to_game_object() for game in self._games.games]
