from typing import TYPE_CHECKING, Union, Tuple, Dict, Optional

if TYPE_CHECKING:
	from . import SessionObject
	from os import PathLike


class Meme():
	"""Base class for :class:`~imgflip.SyncMeme` and :class:`~imgflip.AsyncMeme`
	``str(Meme_object)`` would return the image url of the meme.

	Attributes
	----------
	template_id: :class:`int`
		the id of the meme template
	url: :class:`str`
		the image url of the meme
	page_url: :class:`str`
		the url of the imgflip page of the meme
	"""
	def __init__(
		self,
		template_id: int,
		url: str,
		page_url: str,
		session: "SessionObject"
	):
		self.template_id: int = int(template_id)
		self.url: str = url
		self.page_url: str = page_url
		self.session: SessionObject = session

	def __str__(self) -> str:
		return self.url


class SyncMeme(Meme):
	"""This is a subclass of :class:`~imgflip.Meme`
	It is returned in :meth:`~imgflip.Imgflip.make_meme` when the session passed is ``requests.Session``
	"""
	def read(self) -> bytes:
		"""Read the meme and get the bytes of the image

		Returns
		-------
		:class:`bytes`
		"""
		resp = self.session.get(self.url)
		return resp.content

	def save(self, fp: "PathLike") -> None:
		"""Saves the meme image in a file. This returns nothing.

		Parameters
		----------
		fp: :class:`os.PathLike`
			the file path to save the image to.
		"""
		img = self.read()
		with open(fp, "wb") as f:
			f.write(img)


class AsyncMeme(Meme):
	"""This is a subclass of :class:`~imgflip.Meme`
	It is returned in :meth:`~imgflip.Imgflip.make_meme` when the session passed is ``aiohttp.ClientSession``
	"""
	async def read(self) -> bytes:
		"""|coro|
		Read the meme and get the bytes of the image

		Returns
		-------
		:class:`bytes`
		"""
		async with self.session.get(self.url) as resp:
			img = await resp.read()
		return img

	async def save(self, fp: "PathLike") -> None:
		"""|coro|
		Saves the meme image in a file.

		Parameters
		----------
		fp: :class:`os.PathLike`
			the file path to save the image to.
		"""
		img = await self.read()
		with open(fp, "wb") as f:
			f.write(img)


class Box():
	"""Represents a text box that can be used in the ``boxes`` parameter of :meth:`~imgflip.Imgflip.make_meme`
	``str(Box_object)`` will return the text of the box

	Parameters
	----------
	text: :class:`str`
		the text on the box
	
	position: Tuple[:class:`int`, :class:`int`]
		the position of the box on the meme in the format (x, y)
	
	size: Tuple[:class:`int`, :class:`int`]
		the size of the box in the format (width, height)
	
	color: Optional[:class:`str`]
		the color of the text on the box. Defaults to ``"#ffffff"``
	
	outline_color: Optional[:class:`str`]
		the outline color of the text on the box. Defaults to ``"#000000"``
	"""
	def __init__(
		self,
		text: str,
		position: Tuple[int, int],
		size: Tuple[int, int],
		color: Optional[str] = "#ffffff",
		outline_color: Optional[str] = "#000000"
	):
		self.text: str = text
		self.position: Tuple[int, int] = position
		self.x: int = position[0]
		self.y: int = position[1]
		self.size: Tuple[int, int] = size
		self.width: int = size[0]
		self.height: int = size[1]
		self.color: str = color
		self.outline_color: str = outline_color

		self._raw: Dict[str, Union[str, int]] = {
			"text": text,
			"x": position[0],
			"y": position[1],
			"width": size[0],
			"height": size[1],
			"color": color,
			"outline_color": outline_color
		}

	def __str__(self) -> str:
		"""gets the text of the meme"""
		return self.text

class Template():
	"""Represents a meme template which can be passed into :meth:`~imgflip.Imgflip.make_meme`
	
	.. container:: operations

		.. describe str(x)

			Return the name of the template.
		
		.. describe int(x)

			return the id of the template
	
	Attributes
	----------
	id: :class:`int`
		the template id
	name: Optional[:class:`str`]
		the name of the template
	url: Optional[:class:`str`]
		the image url of the template
	width: Optional[:class:`int`]
		the width of the template image
	height: Optional[:class:`int`]
		the height of the template image
	box_count: Optional[:class:`int`]
		the number of boxes in the template
	"""
	def __init__(
		self,
		id: int,
		name: Optional[str] = None,
		url: Optional[str] = None,
		width: Optional[int] = None,
		height: Optional[int] = None,
		box_count: Optional[int] = None
	):
		self.id: int = int(id)
		self.name: Optional[str] = name
		self.url: Optional[str] = url
		self.width: Optional[int] = int(width)
		self.height: Optional[int] = int(height)
		self.box_count: Optional[int] = int(box_count)

	def __str__(self) -> str:
		"""get the template name"""
		return str(self.name)

	def __int__(self) -> int:
		"""get the template id"""
		return self.id