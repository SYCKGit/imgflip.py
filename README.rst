==========
imgflip.py
==========
Create memes with imgflip easily!

Installation
============
To install, do

.. code-block:: python

    # Linux/macOS
    python3 -m pip install -U imgflip.py

    # Windows
    py -3 -m pip install -U imgflip.py

Examples
========

CLI
---

.. code-block:: python

    py -3 -m imgflip -u USERNAME -p PASSWORD -tname "drake hotline bling" -top "interacting with raw imgflip api" -bot "using imgflip.py"
    # use python3 on Linux/macOS

Result:

.. code-block:: text

    meme created!
    You can find it at: https://imgflip.com/i/5gmxqp
    Image link: https://i.imgflip.com/5gmxqp.jpg

Code
----

Sync

.. code-block:: python

    import imgflip
    import requests

    imgflip_client = imgflip.Imgflip(username="username", password="password", session=requests.Session()) # create an Imgflip instance

    templates = imgflip_client.popular_memes(limit=10) # get popular meme templates from imgflip

    meme = imgflip_client.make_meme(
        template = templates["Drake Hotline Bling"],
        top_text = "interacting with raw imgflip api",
        bottom_text = "using imgflip.py"
    ) # create a meme

    print(meme.url) # print the meme image url

Async

.. code-block:: python

    import imgflip
    import aiohttp
    import asyncio

    async def main():
        async with aiohttp.ClientSession() as session:
            imgflip_client = imgflip.Imgflip(username="username", password="password", session=session) # create an Imgflip instance

            templates = await imgflip_client.popular_memes(limit=10) # get popular meme templates from imgflip

            meme = await imgflip_client.make_meme(
                template = templates["Drake Hotline Bling"],
                top_text = "interacting with raw imgflip api",
                bottom_text = "using imgflip.py"
            ) # create a meme

            print(meme.url) # print the meme image url
    
    asyncio.run(main())

Result:

.. code-block:: text

    https://i.imgflip.com/5f7zzm.jpg

.. image:: https://i.imgflip.com/5f7zzm.jpg
    :alt: the meme that was generated

For documentation, go `here <https://imgflip.readthedocs.io/>`_

Changes in v1.0

* Fixed docstrings
* Added documentation
* Added a command line interface