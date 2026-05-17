import os
import asyncio
import aiohttp
from hydrogram import Client, filters, idle
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# ----- FLASK WEB SERVER FOR RENDER -----
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running 24/7 perfectly on Python 3.14!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=False)

# ⚙️ Configuration Setup
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8639893765:AAEeK8NgH3KUMpzW07HMmnlD8OZRa8HSAZw"
START_IMG = "https://graph.org/file/b7099af5c11783109ea46-2585863078106bcf2c.jpg"

# 🔄 Temporary User Cache for Batch Uploads
USER_DATA = {}

# 🎭 Stylish Text Elements
START_TEXT = (
    "✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ ✨\n\n"
    "I ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ғɪʟᴇs (ᴘʜᴏᴛᴏs, ᴠɪᴅᴇᴏs, ᴀɴɪᴍᴀᴛɪᴏɴs) "
    "ɪɴᴛᴏ ᴀ sᴛ stylɪsʜ ᴀɴᴅ sʜᴀʀᴇᴀʙʟᴇ **ɢʀᴀᴘʜ.ᴏʀɢ** ʟɪɴᴋ ɪɴ sᴇᴄᴏɴᴅs!\n\n"
    "» ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴍᴇᴅɪᴀ ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ."
)

HELP_TEXT = (
    "📖 **ʜᴇʟᴘ & ɢᴜɪᴅᴇ ᴍᴇɴᴜ**\n\n"
    "• **ʜᴏᴡ ᴛᴏ ᴜsᴇ:** sᴇɴᴅ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴘʜᴏᴛᴏs/ᴠɪᴅᴇᴏs ᴛᴏ ᴛʜɪs ᴄʜᴀᴛ.\n"
    "• **ᴘʀᴏᴄᴇssɪɴɢ:** ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀʟʟ ғɪʟᴇs.\n"
    "• **<b>ᴄᴀɴᴄᴇʟ:</b>** ᴜsᴇ /cancel ᴛᴏ ᴄʟᴇᴀʀ ʏᴏᴜʀ sᴇɴᴛ sᴛᴏʀᴀɢᴇ.\n"
    "• **ʟɪᴍɪᴛs:** sᴜᴘᴘᴏʀᴛs ғɪʟᴇs ᴜᴘ ᴛᴏ **𝟻ᴍʙ** ᴘᴇʀ ғɪʟᴇ."
)

ABOUT_TEXT = (
    "🤖 **ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ**\n\n"
    "• **ɴᴀᴍᴇ:** ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅᴇʀ\n"
    "• **ᴜsᴇʀɴᴀᴍᴇ:** @Tele_Conve_link_bot\n"
    "• **ʟᴀɴɢᴜᴀɢᴇ:** ᴘʏᴛʜᴏɴ 𝟹\n"
    "• **ʟɪʙʀᴀʀʏ:** ʜʏᴅʀᴏɢʀᴀᴍ\n\n"
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

# यहाँ हम हैंडलर्स को सीधे रजिस्टर करने के लिए एक फंक्शन का उपयोग करेंगे
def register_handlers(app: Client):
    
    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message: Message):
        await message.reply_photo(photo=START_IMG, caption=START_TEXT, reply_markup=START_BUTTONS)

    @app.on_message(filters.command("cancel") & filters.private)
    async def cancel_action(client, message: Message):
        user_id = message.from_user.id
        if user_id in USER_DATA:
            USER_DATA[user_id].clear()
        await message.reply_text("🧹 `Your temporary file cache has been cleared!`")

    @app.on_callback_query()
    async def callback_handler(client, query):
        user_id = query.from_user.id
        
        if query.data == "help_menu":
            await query.message.edit_caption(caption=HELP_TEXT, reply_markup=BACK_BUTTON)
        elif query.data == "about_menu":
            await query.message.edit_caption(caption=ABOUT_TEXT, reply_markup=BACK_BUTTON)
        elif query.data == "back_home":
            await query.message.edit_caption(caption=START_TEXT, reply_markup=START_BUTTONS)
            
        elif query.data == "generate_links":
            if user_id not in USER_DATA or not USER_DATA[user_id]:
                await query.answer("❌ No files found to process!", show_alert=True)
                return
                
            await query.message.edit_text("🚀 `ᴜᴘʟᴏᴀᴅɪɴɢ ᴀʟʟ ғɪʟᴇs ᴛᴏ ɢʀᴀᴘʜ.ᴏʀɢ...`")
            
            links = []
            for msg in USER_DATA[user_id]:
                try:
                    local_path = await msg.download()
                    upload_url = "https://graph.org/upload"
                    with open(local_path, "rb") as file:
                        form_data = aiohttp.FormData()
                        form_data.add_field("file", file, filename=os.path.basename(local_path))
                        async with aiohttp.ClientSession() as session:
                            async with session.post(upload_url, data=form_data) as response:
                                if response.status == 200:
                                    res_json = await response.json()
                                    file_link = f"https://graph.org{res_json[0]['src']}"
                                    links.append(file_link)
                    if os.path.exists(local_path):
                        os.remove(local_path)
                except Exception:
                    pass
                    
            USER_DATA[user_id].clear()
            
            if links:
                final_text = "📊 **ᴍᴇᴅɪᴀ ᴜᴘʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
                for i, link in enumerate(links, 1):
                    final_text += f"🔗 **ʟɪɴᴋ {i}:** `{link}`\n"
                final_text += "\n🌿 _ᴊᴏɪɴ @MoviesHub_Verse_ ғᴏʀ ᴍᴏʀᴇ ᴜᴘᴅᴀᴛᴇs!_"
                
                result_buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🌐 ᴏᴘᴇɴ ʟɪɴᴋ 𝟷", url=links[0])],
                    [InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url="https://t.me/MoviesHub_Verse")]
                ])
                await query.message.edit_text(text=final_text, reply_markup=result_buttons, disable_web_page_preview=True)
            else:
                await query.message.edit_text("❌ `Templates failed to upload.`")

    @app.on_message((filters.photo | filters.video | filters.animation) & filters.private)
    async def handle_incoming_media(client, message: Message):
        user_id = message.from_user.id
        
        if user_id not in USER_DATA:
            USER_DATA[user_id] = []
            
        USER_DATA[user_id].append(message)
        file_count = len(USER_DATA[user_id])
        
        caption_text = (
            "please click on button after sending all files\n\n"
            f"**Received {file_count} Files.**\n\n"
            "Use /cancel to clear the sent message cache"
        )
        
        process_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Text / Media / Caption", callback_data="generate_links")]
        ])
        
        await message.reply_text(text=caption_text, reply_markup=process_buttons, quote=True)

# 🚀 Safe starter execution inside active event loop
async def main():
    print("--- ⚡ Starting Web Server Thread ⚡ ---")
    Thread(target=run_web, daemon=True).start()
    
    print("--- 🤖 Initializing Hydrogram Client Inside Loop 🤖 ---")
    # Client को यहाँ फंक्शन के अंदर बनाने से इसे पहले से एक्टिव इवेंट लूप मिल जाता है
    app = Client("TelegraphBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    
    # हैंडलर्स रजिस्टर करना
    register_handlers(app)
    
    await app.start()
    print("--- ✨ Bot is Live and Running perfectly without any sync errors! ✨ ---")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
