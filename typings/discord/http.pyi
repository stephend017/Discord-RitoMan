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
log = ...
async def json_or_text(response): # -> Any:
    ...

class Route:
    BASE = ...
    def __init__(self, method, path, **parameters) -> None:
        ...

    @property
    def bucket(self): # -> str:
        ...



class MaybeUnlock:
    def __init__(self, lock) -> None:
        ...

    def __enter__(self): # -> MaybeUnlock:
        ...

    def defer(self): # -> None:
        ...

    def __exit__(self, type, value, traceback): # -> None:
        ...



class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Discord API."""
    SUCCESS_LOG = ...
    REQUEST_LOG = ...
    def __init__(self, connector=..., *, proxy=..., proxy_auth=..., loop=..., unsync_clock=...) -> None:
        ...

    def recreate(self): # -> None:
        ...

    async def ws_connect(self, url, *, compress=...): # -> ClientWebSocketResponse:
        ...

    async def request(self, route, *, files=..., **kwargs): # -> Any | str:
        ...

    async def get_from_cdn(self, url): # -> bytes:
        ...

    async def close(self): # -> None:
        ...

    async def static_login(self, token, *, bot): # -> Any | str:
        ...

    def logout(self): # -> Coroutine[Any, Any, Any | str]:
        ...

    def start_group(self, user_id, recipients): # -> Coroutine[Any, Any, Any | str]:
        ...

    def leave_group(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def add_group_recipient(self, channel_id, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def remove_group_recipient(self, channel_id, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_group(self, channel_id, **options): # -> Coroutine[Any, Any, Any | str]:
        ...

    def convert_group(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def start_private_message(self, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def send_message(self, channel_id, content, *, tts=..., embed=..., nonce=..., allowed_mentions=..., message_reference=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def send_typing(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def send_files(self, channel_id, *, files, content=..., tts=..., embed=..., nonce=..., allowed_mentions=..., message_reference=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    async def ack_message(self, channel_id, message_id): # -> None:
        ...

    def ack_guild(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_message(self, channel_id, message_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_messages(self, channel_id, message_ids, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_message(self, channel_id, message_id, **fields): # -> Coroutine[Any, Any, Any | str]:
        ...

    def add_reaction(self, channel_id, message_id, emoji): # -> Coroutine[Any, Any, Any | str]:
        ...

    def remove_reaction(self, channel_id, message_id, emoji, member_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def remove_own_reaction(self, channel_id, message_id, emoji): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_reaction_users(self, channel_id, message_id, emoji, limit, after=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def clear_reactions(self, channel_id, message_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def clear_single_reaction(self, channel_id, message_id, emoji): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_message(self, channel_id, message_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_channel(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def logs_from(self, channel_id, limit, before=..., after=..., around=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def publish_message(self, channel_id, message_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def pin_message(self, channel_id, message_id, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def unpin_message(self, channel_id, message_id, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def pins_from(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def kick(self, user_id, guild_id, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def ban(self, user_id, guild_id, delete_message_days=..., reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def unban(self, user_id, guild_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def guild_voice_state(self, user_id, guild_id, *, mute=..., deafen=..., reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_profile(self, password, username, avatar, **fields): # -> Coroutine[Any, Any, Any | str]:
        ...

    def change_my_nickname(self, guild_id, nickname, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def change_nickname(self, guild_id, user_id, nickname, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_member(self, guild_id, user_id, *, reason=..., **fields): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_channel(self, channel_id, *, reason=..., **options): # -> Coroutine[Any, Any, Any | str]:
        ...

    def bulk_channel_update(self, guild_id, data, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_channel(self, guild_id, channel_type, *, reason=..., **options): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_channel(self, channel_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_webhook(self, channel_id, *, name, avatar=..., reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def channel_webhooks(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def guild_webhooks(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_webhook(self, webhook_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def follow_webhook(self, channel_id, webhook_channel_id, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_guilds(self, limit, before=..., after=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def leave_guild(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_guild(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_guild(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_guild(self, name, region, icon): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_guild(self, guild_id, *, reason=..., **fields): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_template(self, code): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_from_template(self, code, name, region, icon): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_bans(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_ban(self, user_id, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_vanity_code(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def change_vanity_code(self, guild_id, code, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_all_guild_channels(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_members(self, guild_id, limit, after): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_member(self, guild_id, member_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def prune_members(self, guild_id, days, compute_prune_count, roles, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def estimate_pruned_members(self, guild_id, days): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_all_custom_emojis(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_custom_emoji(self, guild_id, emoji_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_custom_emoji(self, guild_id, name, image, *, roles=..., reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_custom_emoji(self, guild_id, emoji_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_custom_emoji(self, guild_id, emoji_id, *, name, roles=..., reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_all_integrations(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_integration(self, guild_id, type, id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_integration(self, guild_id, integration_id, **payload): # -> Coroutine[Any, Any, Any | str]:
        ...

    def sync_integration(self, guild_id, integration_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_integration(self, guild_id, integration_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_audit_logs(self, guild_id, limit=..., before=..., after=..., user_id=..., action_type=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_widget(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_invite(self, channel_id, *, reason=..., **options): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_invite(self, invite_id, *, with_counts=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def invites_from(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def invites_from_channel(self, channel_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_invite(self, invite_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_roles(self, guild_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_role(self, guild_id, role_id, *, reason=..., **fields): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_role(self, guild_id, role_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def replace_roles(self, user_id, guild_id, role_ids, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def create_role(self, guild_id, *, reason=..., **fields): # -> Coroutine[Any, Any, Any | str]:
        ...

    def move_role_position(self, guild_id, positions, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def add_role(self, guild_id, user_id, role_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def remove_role(self, guild_id, user_id, role_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_channel_permissions(self, channel_id, target, allow, deny, type, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def delete_channel_permissions(self, channel_id, target, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def move_member(self, user_id, guild_id, channel_id, *, reason=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def remove_relationship(self, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def add_relationship(self, user_id, type=...): # -> Coroutine[Any, Any, Any | str]:
        ...

    def send_friend_request(self, username, discriminator): # -> Coroutine[Any, Any, Any | str]:
        ...

    def application_info(self): # -> Coroutine[Any, Any, Any | str]:
        ...

    async def get_gateway(self, *, encoding=..., v=..., zlib=...): # -> str:
        ...

    async def get_bot_gateway(self, *, encoding=..., v=..., zlib=...): # -> tuple[Any | str, str]:
        ...

    def get_user(self, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_user_profile(self, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def get_mutual_friends(self, user_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def change_hypesquad_house(self, house_id): # -> Coroutine[Any, Any, Any | str]:
        ...

    def leave_hypesquad_house(self): # -> Coroutine[Any, Any, Any | str]:
        ...

    def edit_settings(self, **payload): # -> Coroutine[Any, Any, Any | str]:
        ...