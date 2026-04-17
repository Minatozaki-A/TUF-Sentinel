import logging
from services.monitor import get_virtual_memory, get_swap_memory
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import os
from utils.helpers import format_cpu_status, get_formatted_uptime

load_dotenv()
token = os.getenv("TOKEN")
id_user = int(os.getenv("USER_ID"))

only_me = filters.User(user_id=id_user)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def memory_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    vm = get_virtual_memory()
    await update.message.reply_text(
        f'Memory:\n'
        f'Total: {vm.total}\n'
        f'Percent: {vm.percent}\n'
        f'Used: {vm.used}\n'
        f'Free: {vm.free}\n'
        f'Available: {vm.available}\n'
        f'Active: {vm.active}\n'
        f'Inactive: {vm.inactive}\n'
        f'Buffers: {vm.buffers}\n'
        f'Cached: {vm.cached}\n'
        f'Shared: {vm.shared}\n'
    )

async def cpu_info(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    pass

app = ApplicationBuilder().token(token).build()

app.add_handler(MessageHandler(only_me & filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CommandHandler("hello", hello, filters=only_me))
app.add_handler(CommandHandler("memory", memory_info, filters=only_me))
app.add_handler(CommandHandler("cpu", cpu_info, filters=only_me))

app.run_polling()




