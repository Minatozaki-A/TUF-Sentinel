# TUF-Sentinel

A Telegram bot for real-time system monitoring. Exposes CPU, memory, disk, sensor, network, and user metrics via Telegram commands using `psutil`. Access is restricted to a single authorized user.

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
TOKEN=<your_BotFather_token>
USER_ID=<your_telegram_chat_id>
```

- `TOKEN`: bot token from [@BotFather](https://t.me/BotFather).
- `USER_ID`: your numeric Telegram account ID. The bot ignores messages from any other user.

## Running

```bash
uv run main.py
```

## Commands

| Command    | Description                                          |
|------------|------------------------------------------------------|
| `/start`   | Confirm the bot is running                           |
| `/cpu`     | CPU usage, clock frequency, and performance counters |
| `/memory`  | RAM and swap usage                                   |
| `/disks`   | Partitions, disk space usage, and I/O counters       |
| `/sensors` | Component temperatures, fan speeds, and battery      |
| `/network` | Active connections and interface statistics           |
| `/users`   | Logged-in users and time since last boot             |

The bot also sends an automatic general report every hour.

## Project Structure

```
main.py               # Handler registration and bot startup
services/monitor.py   # psutil wrappers grouped by category
utils/
  config.py           # Environment variable loading
  helpers.py          # Output formatting for each report
tools/
  disk_mount.py       # Mount point resolution by disk label
```
