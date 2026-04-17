import logging
from services.monitor import get_virtual_memory, get_swap_memory
import pathlib
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def memory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


app = ApplicationBuilder().token("Token").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("memory",  memory))
app.run_polling()




