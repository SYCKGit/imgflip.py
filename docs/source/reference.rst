=========
Reference
=========

.. |coro| replace:: coroutine
.. _coro: https://docs.python.org/3/library/asyncio-task.html#coroutine

The main class
==============

.. autoclass:: imgflip.Imgflip
    
    .. automethod:: popular_memes

    .. automethod:: make_meme

    .. automethod:: create

    .. automethod:: make

Objects
=======

.. autoclass:: imgflip.Meme

.. autoclass:: imgflip.SyncMeme
    :members:

.. autoclass:: imgflip.AsyncMeme
    :members:

.. autoclass:: imgflip.Box

.. autoclass:: imgflip.Template

Exceptions
==========

.. autoexception:: imgflip.ImgflipError