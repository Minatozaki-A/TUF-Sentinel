import logging
from services.memory_info import get_virtual_memory_info, get_swap_memory_info
import pathlib
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def memory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Memory:\n'
                                    f'{get_virtual_memory_info()}')


app = ApplicationBuilder().token("Token").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("memory",  memory))
app.run_polling()




