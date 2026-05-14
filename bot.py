from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8977764016:AAEf9lhXD4qDFzguoHvxCS7gPu57WiH1dtY"

ADMIN_ID = 7693040685

REGISTER_LINK = "https://13lgame14.com/register?inviteCode=HVS2YBN&from=web"

PREDICTION_CHANNEL = "https://t.me/+Rze4ddKfR944OWZl"

CHANNEL_USERNAME = "https://t.me/+Rze4ddKfR944OWZl"

users = {}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 UID Verification",
                callback_data="uid_verify"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎧 Welcome To13L.geme Customer Service",
        reply_markup=reply_markup
    )


# BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in users:
        users[user_id] = {}

    data = users[user_id]

    # UID VERIFY
    if query.data == "uid_verify":

        data["step"] = "uid"

        await query.message.reply_text(
            "🔍 Send Your UID"
        )

    # CHANNEL REQUEST
    elif query.data == "channel_request":

        data["requested"] = True

        keyboard = [
            [
                InlineKeyboardButton(
                    "🏦 Deposit Problem",
                    callback_data="deposit"
                )
            ],
            [
                InlineKeyboardButton(
                    "💸 Withdraw Problem",
                    callback_data="withdraw"
                )
            ],
            [
                InlineKeyboardButton(
                    "📢 Official Prediction Channel",
                    url=PREDICTION_CHANNEL
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "✅ Request Submitted\n\nSupport Options Unlocked",
            reply_markup=reply_markup
        )

    # DEPOSIT
    elif query.data == "deposit":

        if not data.get("requested"):

            await query.message.reply_text(
                "❌ First Submit Prediction Channel Request"
            )

            return

        data["problem"] = "Deposit"
        data["step"] = "deposit_uid"

        await query.message.reply_text(
            "🆔 Send UID"
        )

    # WITHDRAW
    elif query.data == "withdraw":

        if not data.get("requested"):

            await query.message.reply_text(
                "❌ First Submit Prediction Channel Request"
            )

            return

        data["problem"] = "Withdraw"
        data["step"] = "withdraw_uid"

        await query.message.reply_text(
            "🆔 Send UID"
        )

    # SUBMIT
    elif query.data == "submit":

        caption = f"""
🚨 NEW SUPPORT REQUEST

👤 USERNAME: @{query.from_user.username}

🆔 TELEGRAM ID: {user_id}

🎮 UID: {data.get('uid')}

⚠️ PROBLEM: {data.get('problem')}
"""

        if data.get("problem") == "Deposit":

            caption += f"""

📦 ORDER NUMBER: {data.get('order')}
💳 UTR NUMBER: {data.get('utr')}
"""

        else:

            caption += f"""

📦 WITHDRAW ORDER: {data.get('withdraw_order')}
"""

        await context.bot.send_message(
            ADMIN_ID,
            caption
        )

        photo_keys = [
            "deposit_ss",
            "payment_ss",
            "bank_ss",
            "withdraw_ss",
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

        users.pop(user_id)


# TEXT HANDLER
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in users:
        return

    data = users[user_id]

    step = data.get("step")

    text = update.message.text

    # MAIN UID VERIFY
    if step == "uid":

        if text.startswith("6"):

            data["verified"] = True

            keyboard = [
                [
                    InlineKeyboardButton(
                        "📢 Send Join Request",
                        callback_data="channel_request"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📢 Official Prediction Channel",
                        url=PREDICTION_CHANNEL
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "✅ UID Verified",
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
                "❌ Invalid UID\n\nRegister Now And Send UID Again",
                reply_markup=reply_markup
            )

    # DEPOSIT FLOW
    elif step == "deposit_uid":

        data["uid"] = text
        data["step"] = "deposit_order"

        await update.message.reply_text(
            "📦 Send Order Number"
        )

    elif step == "deposit_order":

        data["order"] = text
        data["step"] = "deposit_utr"

        await update.message.reply_text(
            "💳 Send UTR Number"
        )

    elif step == "deposit_utr":

        data["utr"] = text
        data["step"] = "deposit_ss"

        await update.message.reply_text(
            "📸 Send Deposit Screenshot"
        )

    # WITHDRAW FLOW
    elif step == "withdraw_uid":

        data["uid"] = text
        data["step"] = "withdraw_order"

        await update.message.reply_text(
            "📦 Send Withdraw Order Number"
        )

    elif step == "withdraw_order":

        data["withdraw_order"] = text
        data["step"] = "withdraw_ss"

        await update.message.reply_text(
            "📸 Send Withdraw Screenshot"
        )


# PHOTO HANDLER
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in users:
        return

    data = users[user_id]

    step = data.get("step")

    # DEPOSIT SCREENSHOT
    if step == "deposit_ss":

        data["deposit_ss"] = update.message.message_id
        data["step"] = "payment_ss"

        await update.message.reply_text(
            "💳 Send Payment Screenshot"
        )

    # PAYMENT SCREENSHOT
    elif step == "payment_ss":

        data["payment_ss"] = update.message.message_id
        data["step"] = "bank_ss"

        await update.message.reply_text(
            "🏦 Send Bank Statement Screenshot"
        )

    # BANK SCREENSHOT
    elif step == "bank_ss":

        data["bank_ss"] = update.message.message_id

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Submit Complaint",
                    callback_data="submit"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "✅ All Details Saved",
            reply_markup=reply_markup
        )

    # WITHDRAW SCREENSHOT
    elif step == "withdraw_ss":

        data["withdraw_ss"] = update.message.message_id

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Submit Complaint",
                    callback_data="submit"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "✅ All Details Saved",
            reply_markup=reply_markup
        )


# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(buttons))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_handler
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
