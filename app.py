import os
import threading

from flask import Flask
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# SETTINGS
# =========================

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

# =========================
# COMPANY INFORMATION
# =========================

# =========================
# FLASK
# =========================

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Phenix Visa Bot is running!"


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# =========================
# MAIN MENU
# =========================

def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🇪🇸 اسپانیا", "🇫🇷 فرانسه"],
            ["🇬🇷 یونان", "📋 ارزیابی شرایط من"],
            ["👨‍💼 درخواست مشاوره", "📞 تماس با ما"],
        ],
        resize_keyboard=True,
    )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "🦅 *Phenix Visa*\n\n"
        "سلام 👋\n"
        "به Phenix Visa خوش آمدید.\n\n"
        "ما در زمینه خدمات مهاجرت و اخذ اقامت کشورهای مختلف فعالیت می‌کنیم.\n\n"
        "لطفاً گزینه موردنظر خود را انتخاب کنید.",
        reply_markup=main_keyboard(),
        parse_mode="Markdown",
    )


# =========================
# USER ID
# =========================

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"🆔 Telegram Chat ID شما:\n\n"
        f"`{update.effective_chat.id}`",
        parse_mode="Markdown",
    )


# =========================
# CONTACT MENU
# =========================

async def contact_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📱 Instagram",
                    url="https://instagram.com/phenix.visa"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 WhatsApp",
                    url=f"https://wa.me/+33634810812",
                )
            ],
            [
                InlineKeyboardButton(
                    "📞 تماس با دفتر",
                    url="https://wa.me/982121000013"
                )
            ],
        ]
    )

    await update.message.reply_text(
        "📞 *ارتباط با Phenix Visa*\n\n"
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


# =========================
# COUNTRY SERVICES
# =========================

async def spain(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🇪🇸 *خدمات اسپانیا*\n\n"
        "• 💻 Digital Nomad Visa\n"
        "• 💰 اقامت تمکن مالی\n"
        "• 💼 اقامت کاری\n"
        "• 🏢 ثبت شرکت\n"
        "• 🏠 خرید ملک و سرمایه‌گذاری\n\n"
        "برای بررسی شرایط خود، گزینه «📋 ارزیابی شرایط من» را انتخاب کنید.",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


async def france(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🇫🇷 *خدمات فرانسه*\n\n"
        "• 🎓 ویزای تحصیلی\n"
        "• 💼 ویزای کاری\n"
        "• 🚀 استارتاپ\n"
        "• 🏠 اقامت فرانسه\n\n"
        "برای بررسی شرایط خود، گزینه «📋 ارزیابی شرایط من» را انتخاب کنید.",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


async def greece(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🇬🇷 *خدمات یونان*\n\n"
        "• 🏠 Golden Visa\n"
        "• 💰 اقامت تمکن مالی\n"
        "• 🏢 سرمایه‌گذاری\n"
        "• 🏡 خرید ملک\n\n"
        "برای بررسی شرایط خود، گزینه «📋 ارزیابی شرایط من» را انتخاب کنید.",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================
# START ASSESSMENT
# =========================

async def start_assessment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()
    context.user_data["step"] = "name"

    await update.message.reply_text(
        "📋 *ارزیابی اولیه شرایط مهاجرت*\n\n"
        "این فرم چند سؤال کوتاه دارد.\n"
        "لطفاً اطلاعات را با دقت وارد کنید.\n\n"
        "👤 نام و نام خانوادگی خود را وارد کنید:",
        parse_mode="Markdown",
    )


# =========================
# SEND CUSTOMER TO ADMIN
# =========================

async def send_customer_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not ADMIN_CHAT_ID:
        return

    try:
        admin_id = int(ADMIN_CHAT_ID)
    except ValueError:
        return

    data = context.user_data

    username = update.effective_user.username
    username_text = f"@{username}" if username else "ندارد"

    message = (
        "🔔 *مشتری جدید - Phenix Visa*\n\n"
        f"👤 نام: {data.get('name', '-')}\n"
        f"🎂 سن: {data.get('age', '-')}\n"
        f"💼 شغل: {data.get('job', '-')}\n"
        f"📍 محل اقامت: {data.get('country', '-')}\n"
        f"🎯 کشور مقصد: {data.get('destination', '-')}\n"
        f"💰 درآمد: {data.get('income', '-')}\n"
        f"💵 سرمایه: {data.get('capital', '-')}\n"
        f"💍 وضعیت تأهل: {data.get('marital', '-')}\n"
        f"👶 تعداد فرزندان: {data.get('children', '-')}\n"
        f"📞 شماره تماس: {data.get('phone', '-')}\n\n"
    )

    try:
        await context.bot.send_message(
            chat_id=admin_id,
            text=message,
        )
    except Exception as e:
        print("Admin notification error:", e)


# =========================
# HANDLE CUSTOMER FORM
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    step = context.user_data.get("step")

    # Main menu

    if text == "🇪🇸 اسپانیا":
        await spain(update, context)
        return

    if text == "🇫🇷 فرانسه":
        await france(update, context)
        return

    if text == "🇬🇷 یونان":
        await greece(update, context)
        return

    if text == "📞 تماس با ما":
        await contact_menu(update, context)
        return

    if text == "👨‍💼 درخواست مشاوره":
        context.user_data.clear()
        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "👨‍💼 *درخواست مشاوره*\n\n"
            "لطفاً شماره تماس خود را وارد کنید:",
            parse_mode="Markdown",
        )
        return

    if text == "📋 ارزیابی شرایط من":
        await start_assessment(update, context)
        return

    # Customer assessment

    if step == "name":

        context.user_data["name"] = text
        context.user_data["step"] = "age"

        await update.message.reply_text(
            "🎂 چند سال دارید؟"
        )
        return

    if step == "age":

        context.user_data["age"] = text
        context.user_data["step"] = "job"

        await update.message.reply_text(
            "💼 شغل شما چیست؟"
        )
        return

    if step == "job":

        context.user_data["job"] = text
        context.user_data["step"] = "country"

        await update.message.reply_text(
            "📍 در حال حاضر در کدام کشور زندگی می‌کنید؟"
        )
        return

    if step == "country":

        context.user_data["country"] = text
        context.user_data["step"] = "destination"

        await update.message.reply_text(
            "🎯 برای کدام کشور قصد مهاجرت دارید؟"
        )
        return

    if step == "destination":

        context.user_data["destination"] = text
        context.user_data["step"] = "income"

        await update.message.reply_text(
            "💰 درآمد ماهانه شما تقریباً چقدر است؟\n\n"
            "مثلاً: 3000 یورو"
        )
        return

    if step == "income":

        context.user_data["income"] = text
        context.user_data["step"] = "capital"

        await update.message.reply_text(
            "💵 میزان سرمایه تقریبی شما چقدر است؟"
        )
        return

    if step == "capital":

        context.user_data["capital"] = text
        context.user_data["step"] = "marital"

        await update.message.reply_text(
            "💍 وضعیت تأهل شما چیست؟\n\n"
            "مجرد / متأهل"
        )
        return

    if step == "marital":

        context.user_data["marital"] = text
        context.user_data["step"] = "children"

        await update.message.reply_text(
            "👶 چند فرزند دارید؟"
        )
        return

    if step == "children":

        context.user_data["children"] = text
        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "📞 لطفاً شماره تماس خود را وارد کنید:"
        )
        return

    if step == "phone":

        context.user_data["phone"] = text

        await send_customer_to_admin(update, context)

        await update.message.reply_text(
            "✅ *اطلاعات شما با موفقیت ثبت شد.*\n\n"
            "کارشناسان Phenix Visa شرایط شما را بررسی می‌کنند "
            "و برای ادامه مراحل با شما تماس خواهند گرفت.\n\n"
            "🙏 از اعتماد شما سپاسگزاریم.",
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

        context.user_data.clear()
        return

    await update.message.reply_text(
        "لطفاً یکی از گزینه‌های منوی اصلی را انتخاب کنید.",
        reply_markup=main_keyboard(),
    )


# =========================
# MAIN
# =========================

def main():

    # Start web server for Render
    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True,
    )

    web_thread.start()

    # Start Telegram bot
    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("id", my_id)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Phenix Visa Bot is starting...")

    application.run_polling()


if __name__ == "__main__":
    main()
