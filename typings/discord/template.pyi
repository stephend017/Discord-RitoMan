"""
This type stub file was generated by pyright.
"""

"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
class _FriendlyHttpAttributeErrorHelper:
    __slots__ = ...
    def __getattr__(self, attr): # -> NoReturn:
        ...



class _PartialTemplateState:
    def __init__(self, *, state) -> None:
        ...

    @property
    def is_bot(self):
        ...

    @property
    def shard_count(self):
        ...

    @property
    def user(self):
        ...

    @property
    def self_id(self):
        ...

    @property
    def member_cache_flags(self):
        ...

    def store_emoji(self, guild, packet): # -> None:
        ...

    async def query_members(self, **kwargs): # -> list[Unknown]:
        ...

    def __getattr__(self, attr): # -> NoReturn:
        ...



class Template:
    """Represents a Discord template.

    .. versionadded:: 1.4

    Attributes
    -----------
    code: :class:`str`
        The template code.
    uses: :class:`int`
        How many times the template has been used.
    name: :class:`str`
        The name of the template.
    description: :class:`str`
        The description of the template.
    creator: :class:`User`
        The creator of the template.
    created_at: :class:`datetime.datetime`
        When the template was created.
    updated_at: :class:`datetime.datetime`
        When the template was last updated (referred to as "last synced" in the client).
    source_guild: :class:`Guild`
        The source guild.
    """
    def __init__(self, *, state, data) -> None:
        ...

    def __repr__(self): # -> str:
        ...

    async def create_guild(self, name, region=..., icon=...): # -> Guild:
        """|coro|

        Creates a :class:`.Guild` using the template.

        Bot accounts in more than 10 guilds are not allowed to create guilds.

        Parameters
        ----------
        name: :class:`str`
            The name of the guild.
        region: :class:`.VoiceRegion`
            The region for the voice communication server.
            Defaults to :attr:`.VoiceRegion.us_west`.
        icon: :class:`bytes`
            The :term:`py:bytes-like object` representing the icon. See :meth:`.ClientUser.edit`
            for more details on what is expected.

        Raises
        ------
        :exc:`.HTTPException`
            Guild creation failed.
        :exc:`.InvalidArgument`
            Invalid icon image format given. Must be PNG or JPG.

        Returns
        -------
        :class:`.Guild`
            The guild created. This is not the same guild that is
            added to cache.
        """
        ...
