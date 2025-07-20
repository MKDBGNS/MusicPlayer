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

client = Client("mp", api_id="20014140", api_hash="548622ea394cf4328c47bfd0d45419a0", bot_token="7890433682:AAETDYhwbue9k0nhGhBaxJSbeXRBX7yr_9s")
 
@client.on_message(filters.command("ping"))
async def ping(c, m):
    print("↔ Got /ping")
    await m.reply_text("🟢 Pong!")

@client.on_message(filters.command("test"))
async def test_handler(client, message):
    print("🔔 Received /test command")
    await message.reply_text("✅ Bot is alive!")

if __name__ == "__main__":
    print("🔌 START")
    client.start()
    print("✅ OK", client.me.username)
    idle()
