import os
import json
import shutil
from config import config
from core.song import Song
from pyrogram.types import Message
from pytgcalls import filters as fl
from pyrogram import Client, filters, idle
from pytgcalls.types import Update, ChatUpdate
#from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded
from core.decorators import language, register, only_admins, handle_error
#from pytgcalls.exceptions import (
 #   NotInCallError, GroupCallNotFound, NoActiveGroupCall)
from pytgcalls.exceptions import NotInCallError, NoActiveGroupCall

from core import (
    app, ytdl, safone, search, is_sudo, is_admin, get_group, get_queue,
    pytgcalls, set_group, set_title, all_groups, clear_queue, check_yt_url,
    extract_args, start_stream, shuffle_queue, delete_messages,
    get_spotify_playlist, get_youtube_playlist)

bot = Client(
        "MusicPlayer",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        in_memory=True,)
client = bot
@client.on_message(filters.command("ping"))
async def ping(c, m):
    print("↔ Got /ping")
    await m.reply_text("🟢 Pong!")

@client.on_message(filters.command("test"))
async def test_handler(client, message):
    print("🔔 Received /test command")
    await message.reply_text("✅ Bot is alive!")

@client.on_message(filters.command("start", config.PREFIXES) & ~filters.bot)
@language
@handle_error
async def start(_, message: Message, lang):
    await message.reply_text(lang["startText"] % message.from_user.mention)
 
@client.on_message(filters.command("help", config.PREFIXES) & ~filters.bot)
@language
@handle_error
async def help(_, message: Message, lang):
    await message.reply_text(lang["helpText"].replace("<prefix>", config.PREFIXES[0]))

@client.on_message(filters.command(["p", "play"], config.PREFIXES) & ~filters.private)
@register
@language
@handle_error
async def play_stream(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["admins_only"]:
        check = await is_admin(message)
        if not check:
            k = await message.reply_text(lang["notAllowed"])
            return await delete_messages([message, k])
    song = await search(message)
    if song is None:
        k = await message.reply_text(lang["notFound"])
        return await delete_messages([message, k])
    ok, status = await song.parse()
    if not ok:
        raise Exception(status)
    if not group["is_playing"]:
        set_group(chat_id, is_playing=True, now_playing=song)
        await start_stream(song, lang)
        await delete_messages([message])
    else:
        queue = get_queue(chat_id)
        await queue.put(song)
        k = await message.reply_text(
            lang["addedToQueue"] % (song.title, song.source, len(queue)),
            disable_web_page_preview=True,
        )
        await delete_messages([message, k])


if __name__ == "__main__":
    print("🔌 START")

    client.start()
    print("✅ Pyrogram Started:", client.me.username)

    pytgcalls.start()  # 👈 This is missing!
    print("🎧 PyTgCalls Started")

    idle()

