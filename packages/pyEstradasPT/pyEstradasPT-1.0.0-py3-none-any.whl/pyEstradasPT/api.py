"""API to EstradasPT."""
import logging
from collections import namedtuple
import aiohttp
import json

from .consts import API

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class EstradasPT:
    """Interfaces to Estradas.pt"""

    def __init__(self, websession):
        self.websession = websession

    async def retrieve(self, url, **kwargs):
        """Issue API requests."""
        try:
            async with self.websession.request('GET', url, **kwargs) as res:
                if res.status != 200:
                    raise Exception("Could not retrieve information from API")
                if res.content_type == 'application/json':
                    return await res.json()
                return await res.text()
        except aiohttp.ClientError as err:
            logging.error(err)

    async def liveCameras(self):
        """Retrieve ongoing Cameras"""

        data = await self.retrieve(API)
        data = json.loads(data) # string to json      

        Cameras = namedtuple('Camera', ['id', 'name','url'])

        _cameras = []
        for camera in data['features']:

            _camera = Cameras(camera['attributes']['dbtrafego.telematicadata.EQUIPAMENTOS_DATEX.id'],
                                camera['attributes']['dbtrafego.telematicadata.cctv_url.descricao'],
                                camera['attributes']['dbtrafego.telematicadata.cctv_url.url']
            )
            _cameras.append(_camera)
       
        return _cameras
