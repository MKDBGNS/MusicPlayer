from pyrogram import Client, filters, idle

client = Client("mp", api_id=…, api_hash=…, bot_token=…)

@client.on_message(filters.command("ping"))
async def ping(c, m):
    print("↔ Got /ping")
    await m.reply_text("🟢 Pong!")

if __name__ == "__main__":
    print("🔌 START")
    client.start()
    print("✅ OK", client.me.username)
    idle()
