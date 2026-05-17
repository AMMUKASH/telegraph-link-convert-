import os
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from flask import Flask

# ----- FLASK WEB SERVER FOR RENDER -----
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    # Render ऑटोमैटिकली PORT एनवायरनमेंट वेरिएबल देता है
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# वेब सर्वर को बैकग्राउंड थ्रेड में चलाना
Thread(target=run_web, daemon=True).start()
# ----------------------------------------

# ⚙️ Configuration Setup
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8639893765:AAEeK8NgH3KUMpzW07HMmnlD8OZRa8HSAZw"
START_IMG = "https://graph.org/file/b7099af5c11783109ea46-2585863078106bcf2c.jpg"

app = Client("TelegraphBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🎭 Stylish Text Elements
START_TEXT = (
    "✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ ✨\n\n"
    "I ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ғɪʟᴇs (ᴘʜᴏᴛᴏs, ᴠɪᴅᴇᴏs, ᴀɴɪᴍᴀᴛɪᴏɴs) "
    "ɪɴᴛᴏ ᴀ sᴛ stylɪsʜ ᴀɴᴅ sʜᴀʀᴇᴀʙʟᴇ **ɢʀᴀᴘʜ.ᴏʀɢ** ʟɪɴᴋ ɪɴ sᴇᴄᴏɴᴅs!\n\n"
    "» ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴍᴇᴅɪᴀ ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ."
)

HELP_TEXT = (
    "📖 **ʜᴇʟᴘ & ɢᴜɪᴅᴇ ᴍᴇɴᴜ**\n\n"
    "• **ʜᴏᴡ ᴛᴏ ᴜsᴇ:** ᴊᴜsᴛ sᴇɴᴅ ᴏʀ ғᴏʀᴡᴀʀᴅ ᴀɴʏ ᴘʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, ᴏʀ ɢɪғ ᴛᴏ ᴛʜɪs ᴄʜᴀᴛ.\n"
    "• **ᴘʀᴏᴄᴇssɪɴɢ:** ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴᴅ ɪɴsᴛᴀɴᴛʟʏ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ᴛʜᴇ ᴄʟᴏᴜᴅ.\n"
    "• **ʟɪᴍɪᴛs:** sᴜᴘᴘᴏʀᴛs ғɪʟᴇs ᴜᴘ ᴛᴏ **𝟻ᴍʙ** (ᴀs ᴘᴇʀ ɢʀᴀᴘʜ.ᴏʀɢ ʟɪᴍɪᴛᴀᴛɪᴏɴs)."
)

ABOUT_TEXT = (
    "🤖 **ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ**\n\n"
    "• **ɴᴀᴍᴇ:** ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅᴇʀ\n"
    "• **ᴜsᴇʀɴᴀᴍᴇ:** @Tele_Conve_link_bot\n"
    "• **ʟᴀɴɢᴜᴀɢᴇ:** ᴘʏᴛʜᴏɴ 𝟹\n"
    "• **ʟɪʙʀᴀʀʏ:** ᴘʏʀᴏɢʀᴀᴍ\n\n"
    "⚡ _ᴘᴏᴡᴇʀᴇᴅ ʙʏ @MoviesHub_Verse_"
)

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("⚙️ ʜᴇʟᴘ & ɢᴜɪᴅᴇ", callback_data="help_menu"),
        InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ ʙᴏᴛ", callback_data="about_menu")
    ],
    [InlineKeyboardButton("📢 ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url="https://t.me/MoviesHub_Verse")]
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="back_home")]
])

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_photo(photo=START_IMG, caption=START_TEXT, reply_markup=START_BUTTONS)

@app.on_callback_query()
async def callback_handler(client, query):
    if query.data == "help_menu":
        await query.message.edit_caption(caption=HELP_TEXT, reply_markup=BACK_BUTTON)
    elif query.data == "about_menu":
        await query.message.edit_caption(caption=ABOUT_TEXT, reply_markup=BACK_BUTTON)
    elif query.data == "back_home":
        await query.message.edit_caption(caption=START_TEXT, reply_markup=START_BUTTONS)

@app.on_message((filters.photo | filters.video | filters.animation) & filters.private)
async def telegraph_uploader(client, message: Message):
    status_msg = await message.reply_text("⚡ `ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ᴍᴇᴅɪᴀ...`", quote=True)
    try:
        await status_msg.edit_text("📥 `ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ғɪʟᴇ...`")
        local_path = await message.download()
        await status_msg.edit_text("🚀 `ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ɢʀᴀᴘʜ.ᴏʀɢ...`")
        
        upload_url = "https://graph.org/upload"
        with open(local_path, "rb") as file:
            form_data = aiohttp.FormData()
            form_data.add_field("file", file, filename=os.path.basename(local_path))
            
            async with aiohttp.ClientSession() as session:
                async with session.post(upload_url, data=form_data) as response:
                    if response.status == 200:
                        res_json = await response.json()
                        file_link = f"https://graph.org{res_json[0]['src']}"
                        
                        final_caption = (
                            "📊 **ᴍᴇᴅɪᴀ ᴜᴘʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
                            f"🔗 **ʟɪɴᴋ:** `{file_link}`\n\n"
                            "🌿 _ᴊᴏɪɴ @MoviesHub_Verse_ ᴍᴏʀᴇ ᴜᴘᴅᴀᴛᴇs!_"
                        )
                        result_buttons = InlineKeyboardMarkup([
                            [InlineKeyboardButton("🌐 ᴏᴘᴇɴ ʟɪɴᴋ", url=file_link)],
                            [InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url="https://t.me/MoviesHub_Verse")]
                        ])
                        await status_msg.delete()
                        await message.reply_text(text=final_caption, reply_markup=result_buttons, quote=True)
                    else:
                        await status_msg.edit_text("❌ ``ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴛᴏ sᴇʀᴠᴇʀ.`")
                        
        if os.path.exists(local_path):
            os.remove(local_path)
    except Exception as e:
        await status_msg.edit_text(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`")

print("Bot Status: Active...")
app.run()
