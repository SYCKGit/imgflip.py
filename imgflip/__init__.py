import aiohttp
import requests
from typing import Union, TypeVar, List, Dict, Optional, Literal
from .objects import *
from .models import *
from .errors import ImgflipError

__all__ = (
    "Imgflip",
    "ImgflipError",
    "Meme",
    "Box",
    "Template"
)

__version__ = "1.0"

ImgflipModel = TypeVar("ImgflipModel", SyncModel, AsyncModel)
SessionObject = Union[requests.sessions.Session, aiohttp.client.ClientSession]


class Imgflip():
    """The main Imgflip class

    Parameters
    ----------
    username: :class:`str`
        your imgflip username
    password: :class:`str`
        your imgflip password
    session: Optional[Union[requests.sessions.Session, aiohttp.client.ClientSession]]
        the session which will be used by the class. 
        If it is ``requests.Session``, the methods of this would be sync 
        and if ``aiohttp.ClientSession``, the methods would be async.

    Raises
    ------
    TypeError
        if the session is not ``requests.Session`` or ``aiohttp.ClientSession``
    """
    def __init__(
        self,
        username: str,
        password: str,
        session: Optional[SessionObject] = None
    ):
        if session is None:
            session: requests.sessions.Session = requests.Session()
        if isinstance(session, requests.sessions.Session):
            self._model: ImgflipModel = SyncModel(session)

        elif isinstance(session, aiohttp.client.ClientSession):
            self._model: ImgflipModel = AsyncModel(session)

        else:
            raise TypeError(
                "Expected aiohttp.ClientSession or requests.Session, not "
                + session.__class__.__name__
                + " instead."
            )

        self.username: str = username
        self.password: str = password

    def popular_memes(
        self,
        limit: Optional[int] = 100,
        dictionary: Optional[bool] = True
    ) -> Union[List[Template], Dict[str, Template]]:
        """| This function is a |coro|_ if the session is ``aiohttp.ClientSession``
        | Get the most popular meme templates from imgflip based on 
          how many times they get captioned.

        Parameters
        ----------
        limit: Optional[:class:`int`]
            the amount of templates you want. Defaults to ``100``. 
            You can only get upto ``100`` popular meme templates.
        dictionary: :class:`bool`
            If ``True``, it will return a :class:`dict` with 
            template names as keys and :class:`~imgflip.Template` objects as values

            If ``False``, it will return a :class:`list` of 
            :class:`~imgflip.Template` objects.
        
        Returns
        -------
        Union[List[:class:`~imgflip.Template`], Dict[str, :class:`~imgflip.Template`]]
            the popular meme templates
        """
        if limit > 100:
            limit = 100
        return self._model.get_memes(limit, dictionary)

    def make_meme(
        self,
        template: Union[int, Template],
        font: Literal["impact", "arial"] = "impact",
        max_font_size: Optional[int] = 50,
        top_text: Optional[str] = None,
        bottom_text: Optional[str] = None,
        boxes: Optional[List[Box]] = None
    ) -> Union[SyncMeme, AsyncMeme]:
        """| This function is a |coro|_ if the session is ``aiohttp.ClientSession``
        | Creates a meme.

        Parameters
        ----------
        template: Union[:class:`int`, :class:`~imgflip.Template`]
            the template to use for the meme. You can pass the template id here.
        font: Literal["impact", "arial"]
            the font to use for the text. Defaults to impact.
        max_font_size: Optional[:class:`int`]
            the maximum font size of the text
        top_text: Optional[:class:`str`]
            the text at the top (or the text for the first box) of the meme
        bottom_text: Optional[:class:`str`]
            the text at the bottom (or the text for the second box) of the meme
        boxes: Optional[List[:class:`~imgflip.Box`]]
            the text boxes to use in the meme
        

        .. note::
            if you use top_text/bottom_text and boxes together, 
            boxes would be used in making the meme.
        
        Raises
        ------
        :exc:`~imgflip.ImgflipError`
            Something went wrong while making the meme.
        
        Returns
        -------
        Union[:class:`~imgflip.SyncMeme`, :class:`~imgflip.AsyncMeme`]
            the meme which has been created in imgflip
        """
        font = font.lower().strip()
        if font not in ["impact", "arial"]:
            raise TypeError(
                f"Expected impact or arial font, got {font} instead."
            )

        if (top_text is not None and
            bottom_text is not None and
            boxes is not None):
            top_text = None
            bottom_text = None

        return self._model.caption_image(
            username = self.username,
            password = self.password,
            template_id = template,
            font = font,
            max_font_size = max_font_size,
            text0 = top_text,
            text1 = bottom_text,
            boxes = boxes
        )

    def create(self, *args, **kwargs) -> Union[SyncMeme, AsyncMeme]:
        """alias for :class:`~imgflip.Imgflip.make_meme`"""
        return self.make_meme(*args, **kwargs)

    def make(self, *args, **kwargs) -> Union[SyncMeme, AsyncMeme]:
        """alias for :class:`~imgflip.Imgflip.make_meme`"""
        return self.make_meme(*args, **kwargs)