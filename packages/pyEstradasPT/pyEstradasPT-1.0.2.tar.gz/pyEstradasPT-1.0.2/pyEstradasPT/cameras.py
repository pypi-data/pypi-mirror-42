"""Representation of Cameras."""
import logging
from collections import namedtuple
import aiohttp

from .api import EstradasPT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Cameras:
    """Represents cameras."""

    def __init__(self, websession):
        self.api = EstradasPT(websession)
     
    @classmethod
    async def get(cls, websession):

        self = Cameras(websession)
        self.cameras  = await self.api.liveCameras()
        
        return self

    async def liveCameras(self):
        """Retrieve Live cameras."""

        self.cameras = await self.api.liveCameras()

        return self.cameras
    
    async def UrlByCameraName(self, name):
        """function to return Video URL by camera name."""
        _url=''

        for c in self.cameras:
            if c.name == name:
                _url = c.url
        
        return _url

    async def UrlByCameraId(self, id):
        """function to return Video URL by camera id."""
        _url=''

        for c in self.cameras:
            if c.id == id:
                _url = c.url
        
        return _url


    async def full_list(self):
        """Retrieve ongoing cameras."""

        return self.cameras

    async def number_of_cameras(self):
           
        return len(self.cameras)
