import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
from services.monitor import *
from utils.config import get_user_id, collect_info_by_env


logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s  %(levelname)-8s  %(message)s",
                        datefmt="%H:%M:%S")

TOKEN = collect_info_by_env("TOKEN")
ID_USER = get_user_id("USER_ID")
ONLY_ME = filters.User(user_id=ID_USER)

async def cpu_info(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text(
        collect_cpu_report()
    )

async def memory_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        collect_memory_report()
    )

async def disks_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        collect_disk_report()
    )

async def sensors_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        collect_sensors_report()
    )

async def network_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        collect_network_report()
    )

async def users_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        collect_users_report()
    )

# tarea automática
async def send_report(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id= ID_USER,
        text=collect_general_report(),

    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mensaje recibido")

# comando opcional para probar

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot iniciado para probar.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(ONLY_ME & filters.TEXT & ~filters.COMMAND, handle_text))

    app.add_handler(CommandHandler("memory", memory_info, filters=ONLY_ME))
    app.add_handler(CommandHandler("cpu", cpu_info, filters=ONLY_ME))
    app.add_handler(CommandHandler("disks", disks_info, filters=ONLY_ME))
    app.add_handler(CommandHandler("sensors", sensors_info, filters=ONLY_ME))
    app.add_handler(CommandHandler("network", network_info, filters=ONLY_ME))
    app.add_handler(CommandHandler("users", users_info, filters=ONLY_ME))
    app.add_handler(CommandHandler("start", start))

    # ejecutar cada hora
    app.job_queue.run_repeating(
        callback=send_report,
        interval=3600,  # segundos
        first=10  # empieza después de 10 segundos,
    )

    app.run_polling()

if __name__ == "__main__":
    main()