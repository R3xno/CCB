import random
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from shivu import pm_users as collection


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = escape(update.effective_user.first_name)
    username = update.effective_user.username

    # Check user in database
    user_data = await collection.find_one({"_id": user_id})
    if user_data is None:
        # Add new user to database
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"New user started the bot: <a href='tg://user?id={user_id}'>{first_name}</a>",
            parse_mode='HTML'
        )
    elif user_data.get("first_name") != first_name or user_data.get("username") != username:
        # Update user data if it changed
        await collection.update_one(
            {"_id": user_id},
            {"$set": {"first_name": first_name, "username": username}}
        )

    caption = (
        f"***Heyyyy...***\n\n"
        f"***I am an Open Waifu Catcher Bot! Add me to your group, and I'll send random waifus after "
        f"every 100 messages in the group. Use /guess to collect characters in your collection and "
        f"view your collection with /collection. Add me to your groups and collect your waifus!***"
    )
    keyboard = [
        [InlineKeyboardButton("ADD ME", url=f"http://t.me/{BOT_USERNAME}?startgroup=new")],
        [
            InlineKeyboardButton("SUPPORT", url=f"https://t.me/{SUPPORT_CHAT}"),
            InlineKeyboardButton("UPDATES", url=f"https://t.me/{UPDATE_CHAT}")
        ],
        [InlineKeyboardButton("HELP", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_url = random.choice(PHOTO_URL)

    if update.effective_chat.type == "private":
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_url,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode='markdown'
        )
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_url,
            caption="🎴 I'm alive! Connect with me in PM for more information.",
            reply_markup=reply_markup
        )


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        help_text = (
            "***Help Section:***\n\n"
            "***/guess***: Guess a character (group only).\n"
            "***/fav***: Add your favorite character.\n"
            "***/trade***: Trade characters.\n"
            "***/gift***: Gift a character to another user (group only).\n"
            "***/collection***: View your collection.\n"
            "***/topgroups***: See top groups for waifu guesses.\n"
            "***/top***: See top users.\n"
            "***/ctop***: View your chat leaderboard.\n"
            "***/changetime***: Change character appearance time (group only).\n"
        )
        help_keyboard = [[InlineKeyboardButton("⤾ Back", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        await context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            caption=help_text,
            reply_markup=reply_markup,
            parse_mode='markdown'
        )
    elif query.data == "back":
        caption = (
            f"***Hoyyyy...*** ✨\n\n"
            f"***I am an open-source character catcher bot! Add me to your group, and I'll send random characters "
            f"after every 100 messages. Use /guess to collect characters and /Harem to view your harem. "
            f"Add me to your groups and build your harem!***"
        )
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f"http://t.me/{BOT_USERNAME}?startgroup=new")],
            [
                InlineKeyboardButton("SUPPORT", url=f"https://t.me/{SUPPORT_CHAT}"),
                InlineKeyboardButton("UPDATES", url=f"https://t.me/{UPDATE_CHAT}")
            ],
            [InlineKeyboardButton("HELP", callback_data="help")],
            [InlineKeyboardButton("SOURCE", url="https://t.me/The2B2T")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode='markdown'
        )


# Add handlers
application.add_handler(CallbackQueryHandler(button, pattern="^help$|^back$", block=False))
application.add_handler(CommandHandler("start", start, block=False))
