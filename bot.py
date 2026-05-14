from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8733139795:AAEMhuj0yyk0B8tI-har3VhjgLekgdFeo04"

ADMIN_ID = 6204038568

CHANNEL_USERNAME = "@Roy_op"

REGISTER_LINK = "https://6club11.com/#/register?invitationCode=43646122491"

user_data = {}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    try:
        member = await context.bot.get_chat_member(
            CHANNEL_USERNAME,
            user.id
        )

        if member.status in ["left", "kicked"]:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "Join Prediction Channel",
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
                "❌ Please Join Prediction Channel First",
                reply_markup=reply_markup
            )

            return

    except:
        pass

    user_data[user.id] = {
        "step": "uid"
    }

    await update.message.reply_text(
        "✅ Channel Verified\n\nSend Your UID"
    )


# CHECK JOIN
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user = query.from_user

    member = await context.bot.get_chat_member(
        CHANNEL_USERNAME,
        user.id
    )

    if member.status in ["member", "administrator", "creator"]:

        user_data[user.id] = {
            "step": "uid"
        }

        await query.message.reply_text(
            "✅ Join Successful\n\nNow Send Your UID"
        )

    else:

        await query.message.reply_text(
            "❌ You Have Not Joined Yet"
        )


# MESSAGE HANDLER
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    step = data.get("step")

    # UID STEP
    if step == "uid":

        uid = update.message.text

        if uid.startswith("1"):

            data["uid"] = uid

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

    # DEPOSIT ORDER NUMBER
    elif step == "deposit_order":

        data["deposit_order"] = update.message.text

        data["step"] = "deposit_uid_ss"

        await update.message.reply_text(
            "📸 Send UID Screenshot"
        )

    # WITHDRAW ORDER NUMBER
    elif step == "withdraw_order":

        data["withdraw_order"] = update.message.text

        data["step"] = "withdraw_bank"

        await update.message.reply_text(
            "📄 Send Bank Statement Screenshot"
        )


# BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    # DEPOSIT
    if query.data == "deposit":

        data["problem"] = "Deposit"
        data["step"] = "deposit_ss"

        await query.message.reply_text(
            "📸 Send Deposit Screenshot"
        )

    # WITHDRAW
    elif query.data == "withdraw":

        data["problem"] = "Withdraw"
        data["step"] = "withdraw_ss"

        await query.message.reply_text(
            "📸 Send Withdraw Screenshot"
        )

    # SUBMIT
    elif query.data == "submit":

        caption = f"""
🚨 New Complaint

👤 Username: @{query.from_user.username}

🆔 Telegram ID: {user_id}

🎮 UID: {data.get('uid')}

⚠️ Problem: {data.get('problem')}
"""

        if data.get("problem") == "Deposit":

            caption += f"""

📦 Order Number: {data.get('deposit_order')}
"""

        if data.get("problem") == "Withdraw":

            caption += f"""

📦 Withdraw Order: {data.get('withdraw_order')}
"""

        await context.bot.send_message(
            ADMIN_ID,
            caption
        )

        photo_keys = [
            "deposit_ss",
            "uid_ss",
            "payment_ss",
            "bank_ss",
            "withdraw_ss",
            "withdraw_bank_ss"
        ]

        for key in photo_keys:

            if key in data:

                await context.bot.forward_message(
                    ADMIN_ID,
                    query.message.chat.id,
                    data[key]
                )

        await query.message.reply_text(
            "✅ Complaint Submitted Successfully"
        )

        user_data.pop(user_id)


# PHOTO HANDLER
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    step = data.get("step")

    # DEPOSIT FLOW
    if step == "deposit_ss":

        data["deposit_ss"] = update.message.message_id

        data["step"] = "deposit_order"

        await update.message.reply_text(
            "📦 Send Deposit Order Number"
        )

    elif step == "deposit_uid_ss":

        data["uid_ss"] = update.message.message_id

        data["step"] = "payment_ss"

        await update.message.reply_text(
            "📸 Send Payment Screenshot"
        )

    elif step == "payment_ss":

        data["payment_ss"] = update.message.message_id

        data["step"] = "bank_ss"

        await update.message.reply_text(
            "📄 Send Bank Statement Screenshot"
        )

    elif step == "bank_ss":

        data["bank_ss"] = update.message.message_id

        keyboard = [
            [
                InlineKeyboardButton(
                    "Submit Complaint",
                    callback_data="submit"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "✅ All Proofs Saved\n\nClick Submit Complaint",
            reply_markup=reply_markup
        )

    # WITHDRAW FLOW
    elif step == "withdraw_ss":

        data["withdraw_ss"] = update.message.message_id

        data["step"] = "withdraw_order"

        await update.message.reply_text(
            "📦 Send Withdraw Order Number"
        )

    elif step == "withdraw_bank":

        data["withdraw_bank_ss"] = update.message.message_id

        keyboard = [
            [
                InlineKeyboardButton(
                    "Submit Complaint",
                    callback_data="submit"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "✅ All Proofs Saved\n\nClick Submit Complaint",
            reply_markup=reply_markup
        )


# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(check_join, pattern="check_join")
)

app.add_handler(CallbackQueryHandler(button_handler))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        photo_handler
    )
)

print("Bot Running Successfully...")

app.run_polling()
