import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
from services.monitor import *
from utils.config import get_user_id, get_token


logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s  %(levelname)-8s  %(message)s",
                        datefmt="%H:%M:%S")

token = get_token()
id_user = get_user_id()

only_me = filters.User(user_id=id_user)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

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


app = ApplicationBuilder().token(token).build()

app.add_handler(MessageHandler(only_me & filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CommandHandler("hello", hello, filters=only_me))
app.add_handler(CommandHandler("memory", memory_info, filters=only_me))
app.add_handler(CommandHandler("cpu", cpu_info, filters=only_me))
app.add_handler(CommandHandler("disks", disks_info, filters=only_me))
app.add_handler(CommandHandler("sensors", sensors_info, filters=only_me))
app.add_handler(CommandHandler("network", network_info, filters=only_me))
app.add_handler(CommandHandler("users", users_info, filters=only_me))

app.run_polling()