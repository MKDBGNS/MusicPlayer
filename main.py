from pyrogram import Client, filters, idle

client = Client("mp", api_id=20014140, api_hash=548622ea394cf4328c47bfd0d45419a0, bot_token=7890433682:AAETDYhwbue9k0nhGhBaxJSbeXRBX7yr_9s)
 
@client.on_message(filters.command("ping"))
async def ping(c, m):
    print("↔ Got /ping")
    await m.reply_text("🟢 Pong!")

if __name__ == "__main__":
    print("🔌 START")
    client.start()
    print("✅ OK", client.me.username)
    idle()
