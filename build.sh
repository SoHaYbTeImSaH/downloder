#!/bin/sh

# ایجاد محیط مجازی
python -m venv /opt/venv

# فعال کردن محیط مجازی
. /opt/venv/bin/activate

# نصب requests
pip install requests

# نصب python-telegram-bot
pip install python-telegram-bot --no-cache-dir
