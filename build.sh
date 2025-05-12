#!/bin/sh

# Activate venv
python -m venv /opt/venv
. /opt/venv/bin/activate

# Install dependencies
pip install requests

# Install python-telegram-bot with dependencies fixed
pip install python-telegram-bot --no-cache-dir --ignore-installed
