import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import os
from services.monitor import information_cpu, information_memory, information_disk, information_sensors, information_network, information_users

logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s  %(levelname)-8s  %(message)s",
                        datefmt="%H:%M:%S")
load_dotenv()
token = os.getenv("TOKEN")
id_user = int(os.getenv("USER_ID"))

only_me = filters.User(user_id=id_user)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def cpu_info(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text(
        information_cpu()
    )

async def memory_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        information_memory()
    )


async def disks_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        information_disk("/")
    )

async def sensors_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        information_sensors()
    )

async def network_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        information_network()
    )

async def users_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        information_users()
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