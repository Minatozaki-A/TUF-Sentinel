import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import os
from utils.helpers import *
from services.monitor import *

load_dotenv()
token = os.getenv("TOKEN")
id_user = int(os.getenv("USER_ID"))

only_me = filters.User(user_id=id_user)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def memory_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    vm = get_virtual_memory()
    swap = get_swap_memory()
    await update.message.reply_text(
        format_memory(vm, swap)
    )

async def cpu_info(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    cpu_percent = get_cpu_percent()
    cpu_freq = get_cpu_freq()
    cpu_stats = get_cpu_stats()
    await update.message.reply_text(
        format_cpu(cpu_percent, cpu_freq, cpu_stats)
    )

async def disks_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    disks_partitions = get_disk_partitions()
    disk_usage = get_disk_usage("/")
    disks_io_counters = get_disk_io_counters()
    await update.message.reply_text(
        format_disks(disks_partitions, disk_usage, disks_io_counters)
    )

async def sensors_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sensors_temperatures = get_sensors_temperatures()
    sensors_fans = get_sensors_fans()
    sensors_battery = get_sensors_battery()
    await update.message.reply_text(
        format_sensors(sensors_temperatures, sensors_fans, sensors_battery)
    )


app = ApplicationBuilder().token(token).build()

app.add_handler(MessageHandler(only_me & filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CommandHandler("hello", hello, filters=only_me))
app.add_handler(CommandHandler("memory", memory_info, filters=only_me))
app.add_handler(CommandHandler("cpu", cpu_info, filters=only_me))
app.add_handler(CommandHandler("disks", disks_info, filters=only_me))
app.add_handler(CommandHandler("sensors", sensors_info, filters=only_me))

app.run_polling()




