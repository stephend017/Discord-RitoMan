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
class _RawReprMixin:
    def __repr__(self): # -> str:
        ...



class RawMessageDeleteEvent(_RawReprMixin):
    """Represents the event payload for a :func:`on_raw_message_delete` event.

    Attributes
    ------------
    channel_id: :class:`int`
        The channel ID where the deletion took place.
    guild_id: Optional[:class:`int`]
        The guild ID where the deletion took place, if applicable.
    message_id: :class:`int`
        The message ID that got deleted.
    cached_message: Optional[:class:`Message`]
        The cached message, if found in the internal message cache.
    """
    __slots__ = ...
    def __init__(self, data) -> None:
        ...



class RawBulkMessageDeleteEvent(_RawReprMixin):
    """Represents the event payload for a :func:`on_raw_bulk_message_delete` event.

    Attributes
    -----------
    message_ids: Set[:class:`int`]
        A :class:`set` of the message IDs that were deleted.
    channel_id: :class:`int`
        The channel ID where the message got deleted.
    guild_id: Optional[:class:`int`]
        The guild ID where the message got deleted, if applicable.
    cached_messages: List[:class:`Message`]
        The cached messages, if found in the internal message cache.
    """
    __slots__ = ...
    def __init__(self, data) -> None:
        ...



class RawMessageUpdateEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_message_edit` event.

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got updated.
    channel_id: :class:`int`
        The channel ID where the update took place.

        .. versionadded:: 1.3

    data: :class:`dict`
        The raw data given by the `gateway <https://discord.com/developers/docs/topics/gateway#message-update>`_
    cached_message: Optional[:class:`Message`]
        The cached message, if found in the internal message cache.
    """
    __slots__ = ...
    def __init__(self, data) -> None:
        ...



class RawReactionActionEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_reaction_add` or
    :func:`on_raw_reaction_remove` event.

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got or lost a reaction.
    user_id: :class:`int`
        The user ID who added the reaction or whose reaction was removed.
    channel_id: :class:`int`
        The channel ID where the reaction got added or removed.
    guild_id: Optional[:class:`int`]
        The guild ID where the reaction got added or removed, if applicable.
    emoji: :class:`PartialEmoji`
        The custom or unicode emoji being used.
    member: Optional[:class:`Member`]
        The member who added the reaction. Only available if `event_type` is `REACTION_ADD` and the reaction is inside a guild.

        .. versionadded:: 1.3

    event_type: :class:`str`
        The event type that triggered this action. Can be
        ``REACTION_ADD`` for reaction addition or
        ``REACTION_REMOVE`` for reaction removal.

        .. versionadded:: 1.3
    """
    __slots__ = ...
    def __init__(self, data, emoji, event_type) -> None:
        ...



class RawReactionClearEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_reaction_clear` event.

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got its reactions cleared.
    channel_id: :class:`int`
        The channel ID where the reactions got cleared.
    guild_id: Optional[:class:`int`]
        The guild ID where the reactions got cleared.
    """
    __slots__ = ...
    def __init__(self, data) -> None:
        ...



class RawReactionClearEmojiEvent(_RawReprMixin):
    """Represents the payload for a :func:`on_raw_reaction_clear_emoji` event.

    .. versionadded:: 1.3

    Attributes
    -----------
    message_id: :class:`int`
        The message ID that got its reactions cleared.
    channel_id: :class:`int`
        The channel ID where the reactions got cleared.
    guild_id: Optional[:class:`int`]
        The guild ID where the reactions got cleared.
    emoji: :class:`PartialEmoji`
        The custom or unicode emoji being removed.
    """
    __slots__ = ...
    def __init__(self, data, emoji) -> None:
        ...
