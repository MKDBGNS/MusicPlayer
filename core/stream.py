"""
Music Player, Telegram Voice Chat Bot
Copyright (c) 2021-present Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

"""
Music Player, Telegram Voice Chat Bot
Licensed under GNU AGPL v3. See <https://www.gnu.org/licenses/> for details.
"""

import os
from config import config
from core.song import Song
from pyrogram import Client
from yt_dlp import YoutubeDL
from pytgcalls import PyTgCalls
from core.funcs import generate_cover
from core.groups import get_group, set_title
from pytgcalls.types.stream import MediaStream
from pytgcalls.types import AudioQuality, VideoQuality
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.exceptions import NotInCallError

# Stream message tracking per chat
safone = {}

# YT-DLP options
ydl_opts = {
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}
ytdl = YoutubeDL(ydl_opts)

# Pyrogram Client
app = Client(
    "MusicPlayerUB",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION,
    in_memory=True,
)

# PyTgCalls Client
pytgcalls = PyTgCalls(app)


async def start_stream(chat_id: int, song: Song, lang: dict):
    chat = song.request_msg.chat

    # Remove old stream message if exists
    if safone.get(chat.id):
        try:
            await safone[chat.id].delete()
        except Exception:
            pass

    infomsg = await song.request_msg.reply_text(lang["downloading"])

    # Retry logic for GroupCall errors
    for _ in range(3):
        try:
            await pytgcalls.join_group_call(
                chat.id,
                get_quality(song),
                stream_type=StreamType().local_stream)

            break
        except NotInCallError:
            peer = await app.resolve_peer(chat.id)
            await app.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    ),
                    random_id=app.rnd_id() // 9000000000,
                )
            )
    else:
        return await infomsg.edit_text("⚠️ Failed to start stream after multiple retries.")

    await set_title(chat.id, song.title, client=app)

    # Generate thumbnail
    thumb = await generate_cover(song.title, chat.title, chat.id, song.thumb)

    # Send stream photo
    safone[chat.id] = await song.request_msg.reply_photo(
        photo=thumb,
        caption=lang["playing"] % (
            song.title,
            song.source,
            song.duration,
            song.request_msg.chat.id,
            (
                song.requested_by.mention
                if song.requested_by
                else song.request_msg.sender_chat.title
            ),
        ),
        quote=False,
    )

    await infomsg.delete()

    # Safe cleanup for thumbnail
    try:
        if os.path.exists(thumb):
            os.remove(thumb)
    except Exception as e:
        print(f"Thumbnail cleanup failed: {e}")


def get_quality(song: Song) -> MediaStream:
    group = get_group(song.request_msg.chat.id)
    quality = config.QUALITY.lower()

    video_stream = group["stream_mode"] == "video"

    # Quality preset mapping
    presets = {
        "high": (AudioQuality.HIGH, VideoQuality.FHD_1080p),
        "medium": (AudioQuality.MEDIUM, VideoQuality.HD_720p),
        "low": (AudioQuality.LOW, VideoQuality.SD_480p),
    }

    # Fallback to high if invalid
    if quality not in presets:
        print("WARNING: Invalid QUALITY. Defaulting to High!")
        quality = "high"

    audio_quality, video_quality = presets[quality]

    if video_stream:
        return MediaStream(
            song.remote,
            audio_quality,
            video_quality,
            headers=song.headers,
        )
    else:
        return MediaStream(
            song.remote,
            audio_quality,
            video_flags=MediaStream.Flags.IGNORE,
            headers=song.headers,
        )
