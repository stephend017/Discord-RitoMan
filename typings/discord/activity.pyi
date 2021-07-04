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
class BaseActivity:
    """The base activity that all user-settable activities inherit from.
    A user-settable activity is one that can be used in :meth:`Client.change_presence`.

    The following types currently count as user-settable:

    - :class:`Activity`
    - :class:`Game`
    - :class:`Streaming`
    - :class:`CustomActivity`

    Note that although these types are considered user-settable by the library,
    Discord typically ignores certain combinations of activity depending on
    what is currently set. This behaviour may change in the future so there are
    no guarantees on whether Discord will actually let you set these types.

    .. versionadded:: 1.3
    """
    __slots__ = ...
    def __init__(self, **kwargs) -> None:
        ...

    @property
    def created_at(self): # -> datetime | None:
        """Optional[:class:`datetime.datetime`]: When the user started doing this activity in UTC.

        .. versionadded:: 1.3
        """
        ...



class Activity(BaseActivity):
    """Represents an activity in Discord.

    This could be an activity such as streaming, playing, listening
    or watching.

    For memory optimisation purposes, some activities are offered in slimmed
    down versions:

    - :class:`Game`
    - :class:`Streaming`

    Attributes
    ------------
    application_id: :class:`int`
        The application ID of the game.
    name: :class:`str`
        The name of the activity.
    url: :class:`str`
        A stream URL that the activity could be doing.
    type: :class:`ActivityType`
        The type of activity currently being done.
    state: :class:`str`
        The user's current state. For example, "In Game".
    details: :class:`str`
        The detail of the user's current activity.
    timestamps: :class:`dict`
        A dictionary of timestamps. It contains the following optional keys:

        - ``start``: Corresponds to when the user started doing the
          activity in milliseconds since Unix epoch.
        - ``end``: Corresponds to when the user will finish doing the
          activity in milliseconds since Unix epoch.

    assets: :class:`dict`
        A dictionary representing the images and their hover text of an activity.
        It contains the following optional keys:

        - ``large_image``: A string representing the ID for the large image asset.
        - ``large_text``: A string representing the text when hovering over the large image asset.
        - ``small_image``: A string representing the ID for the small image asset.
        - ``small_text``: A string representing the text when hovering over the small image asset.

    party: :class:`dict`
        A dictionary representing the activity party. It contains the following optional keys:

        - ``id``: A string representing the party ID.
        - ``size``: A list of up to two integer elements denoting (current_size, maximum_size).
    emoji: Optional[:class:`PartialEmoji`]
        The emoji that belongs to this activity.
    """
    __slots__ = ...
    def __init__(self, **kwargs) -> None:
        ...

    def __repr__(self): # -> str:
        ...

    def to_dict(self): # -> dict[Unknown, Unknown]:
        ...

    @property
    def start(self): # -> datetime | None:
        """Optional[:class:`datetime.datetime`]: When the user started doing this activity in UTC, if applicable."""
        ...

    @property
    def end(self): # -> datetime | None:
        """Optional[:class:`datetime.datetime`]: When the user will stop doing this activity in UTC, if applicable."""
        ...

    @property
    def large_image_url(self): # -> str | None:
        """Optional[:class:`str`]: Returns a URL pointing to the large image asset of this activity if applicable."""
        ...

    @property
    def small_image_url(self): # -> str | None:
        """Optional[:class:`str`]: Returns a URL pointing to the small image asset of this activity if applicable."""
        ...

    @property
    def large_image_text(self): # -> Any | None:
        """Optional[:class:`str`]: Returns the large image asset hover text of this activity if applicable."""
        ...

    @property
    def small_image_text(self): # -> Any | None:
        """Optional[:class:`str`]: Returns the small image asset hover text of this activity if applicable."""
        ...



class Game(BaseActivity):
    """A slimmed down version of :class:`Activity` that represents a Discord game.

    This is typically displayed via **Playing** on the official Discord client.

    .. container:: operations

        .. describe:: x == y

            Checks if two games are equal.

        .. describe:: x != y

            Checks if two games are not equal.

        .. describe:: hash(x)

            Returns the game's hash.

        .. describe:: str(x)

            Returns the game's name.

    Parameters
    -----------
    name: :class:`str`
        The game's name.
    start: Optional[:class:`datetime.datetime`]
        A naive UTC timestamp representing when the game started. Keyword-only parameter. Ignored for bots.
    end: Optional[:class:`datetime.datetime`]
        A naive UTC timestamp representing when the game ends. Keyword-only parameter. Ignored for bots.

    Attributes
    -----------
    name: :class:`str`
        The game's name.
    """
    __slots__ = ...
    def __init__(self, name, **extra) -> None:
        ...

    @property
    def type(self): # -> int:
        """:class:`ActivityType`: Returns the game's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.playing`.
        """
        ...

    @property
    def start(self): # -> datetime | None:
        """Optional[:class:`datetime.datetime`]: When the user started playing this game in UTC, if applicable."""
        ...

    @property
    def end(self): # -> datetime | None:
        """Optional[:class:`datetime.datetime`]: When the user will stop playing this game in UTC, if applicable."""
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self): # -> str:
        ...

    def to_dict(self): # -> dict[str, Unknown | str | dict[Unknown, Unknown]]:
        ...

    def __eq__(self, other) -> bool:
        ...

    def __ne__(self, other) -> bool:
        ...

    def __hash__(self) -> int:
        ...



class Streaming(BaseActivity):
    """A slimmed down version of :class:`Activity` that represents a Discord streaming status.

    This is typically displayed via **Streaming** on the official Discord client.

    .. container:: operations

        .. describe:: x == y

            Checks if two streams are equal.

        .. describe:: x != y

            Checks if two streams are not equal.

        .. describe:: hash(x)

            Returns the stream's hash.

        .. describe:: str(x)

            Returns the stream's name.

    Attributes
    -----------
    platform: :class:`str`
        Where the user is streaming from (ie. YouTube, Twitch).

        .. versionadded:: 1.3

    name: Optional[:class:`str`]
        The stream's name.
    details: Optional[:class:`str`]
        An alias for :attr:`name`
    game: Optional[:class:`str`]
        The game being streamed.

        .. versionadded:: 1.3

    url: :class:`str`
        The stream's URL.
    assets: :class:`dict`
        A dictionary comprising of similar keys than those in :attr:`Activity.assets`.
    """
    __slots__ = ...
    def __init__(self, *, name, url, **extra) -> None:
        ...

    @property
    def type(self): # -> int:
        """:class:`ActivityType`: Returns the game's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.streaming`.
        """
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self): # -> str:
        ...

    @property
    def twitch_name(self): # -> Any | None:
        """Optional[:class:`str`]: If provided, the twitch name of the user streaming.

        This corresponds to the ``large_image`` key of the :attr:`Streaming.assets`
        dictionary if it starts with ``twitch:``. Typically set by the Discord client.
        """
        ...

    def to_dict(self): # -> dict[str, Unknown | str | dict[Any, Any]]:
        ...

    def __eq__(self, other) -> bool:
        ...

    def __ne__(self, other) -> bool:
        ...

    def __hash__(self) -> int:
        ...



class Spotify:
    """Represents a Spotify listening activity from Discord. This is a special case of
    :class:`Activity` that makes it easier to work with the Spotify integration.

    .. container:: operations

        .. describe:: x == y

            Checks if two activities are equal.

        .. describe:: x != y

            Checks if two activities are not equal.

        .. describe:: hash(x)

            Returns the activity's hash.

        .. describe:: str(x)

            Returns the string 'Spotify'.
    """
    __slots__ = ...
    def __init__(self, **data) -> None:
        ...

    @property
    def type(self): # -> int:
        """:class:`ActivityType`: Returns the activity's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.listening`.
        """
        ...

    @property
    def created_at(self): # -> datetime | None:
        """Optional[:class:`datetime.datetime`]: When the user started listening in UTC.

        .. versionadded:: 1.3
        """
        ...

    @property
    def colour(self): # -> Colour:
        """:class:`Colour`: Returns the Spotify integration colour, as a :class:`Colour`.

        There is an alias for this named :attr:`color`"""
        ...

    @property
    def color(self): # -> Colour:
        """:class:`Colour`: Returns the Spotify integration colour, as a :class:`Colour`.

        There is an alias for this named :attr:`colour`"""
        ...

    def to_dict(self): # -> dict[str, int | str | Unknown | dict[Any, Any] | None]:
        ...

    @property
    def name(self): # -> Literal['Spotify']:
        """:class:`str`: The activity's name. This will always return "Spotify"."""
        ...

    def __eq__(self, other) -> bool:
        ...

    def __ne__(self, other) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self): # -> str:
        ...

    @property
    def title(self): # -> None:
        """:class:`str`: The title of the song being played."""
        ...

    @property
    def artists(self):
        """List[:class:`str`]: The artists of the song being played."""
        ...

    @property
    def artist(self): # -> None:
        """:class:`str`: The artist of the song being played.

        This does not attempt to split the artist information into
        multiple artists. Useful if there's only a single artist.
        """
        ...

    @property
    def album(self): # -> Any | str:
        """:class:`str`: The album that the song being played belongs to."""
        ...

    @property
    def album_cover_url(self): # -> Any | str:
        """:class:`str`: The album cover image URL from Spotify's CDN."""
        ...

    @property
    def track_id(self):
        """:class:`str`: The track ID used by Spotify to identify this song."""
        ...

    @property
    def start(self): # -> datetime:
        """:class:`datetime.datetime`: When the user started playing this song in UTC."""
        ...

    @property
    def end(self): # -> datetime:
        """:class:`datetime.datetime`: When the user will stop playing this song in UTC."""
        ...

    @property
    def duration(self): # -> timedelta:
        """:class:`datetime.timedelta`: The duration of the song being played."""
        ...

    @property
    def party_id(self): # -> Any | str:
        """:class:`str`: The party ID of the listening party."""
        ...



class CustomActivity(BaseActivity):
    """Represents a Custom activity from Discord.

    .. container:: operations

        .. describe:: x == y

            Checks if two activities are equal.

        .. describe:: x != y

            Checks if two activities are not equal.

        .. describe:: hash(x)

            Returns the activity's hash.

        .. describe:: str(x)

            Returns the custom status text.

    .. versionadded:: 1.3

    Attributes
    -----------
    name: Optional[:class:`str`]
        The custom activity's name.
    emoji: Optional[:class:`PartialEmoji`]
        The emoji to pass to the activity, if any.
    """
    __slots__ = ...
    def __init__(self, name, *, emoji=..., **extra) -> None:
        ...

    @property
    def type(self): # -> int:
        """:class:`ActivityType`: Returns the activity's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.custom`.
        """
        ...

    def to_dict(self): # -> dict[str, Unknown | str | None] | dict[str, Unknown | None]:
        ...

    def __eq__(self, other) -> bool:
        ...

    def __ne__(self, other) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self): # -> str:
        ...



def create_activity(data): # -> Activity | Game | CustomActivity | Streaming | Spotify | None:
    ...
