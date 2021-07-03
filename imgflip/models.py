from .objects import *
from .errors import ImgflipError

BASE_URL = "https://api.imgflip.com"


class SyncModel():
	def __init__(self, session):
		self.session = session

	def get_memes(self, limit, dictionary):
		resp = self.session.get(f"{BASE_URL}/get_memes")
		memes = resp.json()["data"]["memes"][:limit]

		if dictionary is False:
			return [Template(**meme) for meme in memes.values()]

		return {meme["name"]: Template(**meme) for meme in memes}

	def caption_image(self, **kwargs):
		kwargs["template_id"] = int(kwargs["template_id"])
		data = kwargs.copy()

		for k, v in kwargs.items():
			if v is None:
				del data[k]

		if data.get("boxes") is not None:
			boxes = dict()

			for index, box in enumerate(data.get("boxes")):
				for k, v in box._raw.items():
					boxes[f"boxes[{index}][{k}]"] = v

			del data["boxes"]
			data.update(boxes)

		data["max_font_size"] = f"{data['max_font_size']}px"

		resp = self.session.post(f"{BASE_URL}/caption_image", params=data)
		resp_json = resp.json()

		if resp_json["success"] is False:
			raise ImgflipError(resp_json["error_message"])

		meme = SyncMeme(
			template_id=kwargs["template_id"],
			session=self.session,
			**(resp_json["data"])
		)
		return meme


class AsyncModel():
	def __init__(self, session):
		self.session = session

	async def get_memes(self, limit, dictionary):
		async with self.session.get(f"{BASE_URL}/get_memes") as resp:
			memes = (await resp.json())["data"]["memes"][:limit]

		if dictionary is False:
			return [Template(**meme) for meme in memes.values()]

		return {meme["name"]: Template(**meme) for meme in memes}

	async def caption_image(self, **kwargs):
		kwargs["template_id"] = int(kwargs["template_id"])
		data = kwargs.copy()
	
		for k, v in kwargs.items():
			if v is None:
				del data[k]

		if data.get("boxes") is not None:
			boxes = dict()

			for index, box in enumerate(data.get("boxes")):
				for k, v in box._raw.items():
					boxes[f"boxes[{index}][{k}]"] = v

			del data["boxes"]
			data.update(boxes)

		data["max_font_size"] = f"{data['max_font_size']}px"

		async with self.session.post(
			f"{BASE_URL}/caption_image", params=data
		) as resp:
			resp_json = await resp.json()
			if resp_json["success"] is False:
				raise ImgflipError(resp_json["error_message"])

			meme = AsyncMeme(
				template_id=kwargs["template_id"],
				session=self.session,
				**(resp_json["data"])
			)
		return meme