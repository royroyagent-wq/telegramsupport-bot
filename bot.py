from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "YOUR_BOT_TOKEN"

ADMIN_ID = 6204038568

CHANNEL_USERNAME = "@Roy_op"

REGISTER_LINK = "https://6club11.com/#/register?invitationCode=43646122491"


user_data_dict = {}


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    member = await context.bot.get_chat_member(
        CHANNEL_USERNAME,
        user.id
    )

    if member.status in ["left", "kicked"]:

        keyboard = [
            [
                InlineKeyboardButton(
                    "Join Channel",
                    url="https://t.me/Roy_op"
                )
            ],
            [
                InlineKeyboardButton(
                    "Check Joined",
                    callback_data="check_join"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ Please Join Our Prediction Channel First",
            reply_markup=reply_markup
        )

        return

    await update.message.reply_text(
        "✅ Channel Verified\n\nSend Your UID"
    )


# CHECK JOIN BUTTON
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user = query.from_user

    member = await context.bot.get_chat_member(
        CHANNEL_USERNAME,
        user.id
    )

    if member.status in ["member", "administrator", "creator"]:

        await query.message.reply_text(
            "✅ Join Successful\n\nNow Send Your UID"
        )

    else:

        await query.message.reply_text(
            "❌ You Still Have Not Joined Channel"
        )


# UID CHECK
async def uid_check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.message.text

    if uid.startswith("1"):

        user_data_dict[update.effective_user.id] = {
            "uid": uid
        }

        keyboard = [
            [
                InlineKeyboardButton(
                    "Deposit Problem",
                    callback_data="deposit"
                )
            ],
            [
                InlineKeyboardButton(
                    "Withdraw Problem",
                    callback_data="withdraw"
                )
            ],
            [
                InlineKeyboardButton(
                    "Prediction Channel",
                    url="https://t.me/Roy_op"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "✅ UID Verified\n\nSelect Your Problem",
            reply_markup=reply_markup
        )

    else:

        keyboard = [
            [
                InlineKeyboardButton(
                    "Register Now",
                    url=REGISTER_LINK
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ Invalid UID\n\nRegister From Our Link",
            reply_markup=reply_markup
        )


# BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "deposit":

        user_data_dict[query.from_user.id]["problem"] = "Deposit"

        await query.message.reply_text(
            "Send Deposit Screenshot"
        )

    elif query.data == "withdraw":

        user_data_dict[query.from_user.id]["problem"] = "Withdraw"

        await query.message.reply_text(
            "Send Withdraw Screenshot"
        )


# PHOTO HANDLER
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_data_dict:
        return

    data = user_data_dict[user_id]

    uid = data["uid"]
    problem = data["problem"]

    caption = f"""
🚨 New Complaint

👤 User: @{update.effective_user.username}

🆔 UID: {uid}

⚠ Problem: {problem}
"""

    await context.bot.send_message(
        ADMIN_ID,
        caption
    )

    await context.bot.forward_message(
        ADMIN_ID,
        update.message.chat.id,
        update.message.message_id
    )

    await update.message.reply_text(
        "✅ Complaint Submitted Successfully"
    )


# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

app.add_handler(CallbackQueryHandler(button_handler))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, uid_check))

app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

print("Bot Running...")

app.run_polling()
