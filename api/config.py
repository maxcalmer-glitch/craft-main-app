#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Конфигурация
"""

import os


class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL', '')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    BLOCK_VIDEO_FILE_ID = 'BAACAgIAAxkBAAOPaZmixiXAHFgMJLNMtbTQX58vziAAAoeGAAL0dMlI27YW0zTjlMg6BA'
    REQUIRED_CHANNEL_ID = os.environ.get('REQUIRED_CHANNEL_ID', '-1003420440477')
    ADMIN_CHAT_APPLICATIONS = os.environ.get('ADMIN_CHAT_APPLICATIONS', '-5077929004')
    ADMIN_CHAT_SOS = os.environ.get('ADMIN_CHAT_SOS', '-4896709682')
    ADMIN_CHAT_SUPPORT = os.environ.get('ADMIN_CHAT_SUPPORT', '-5059607831')
    APP_URL = os.environ.get('APP_URL', 'https://craft-main-app.vercel.app')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    AI_MODEL = 'gpt-4o-mini'
    AI_COST_PER_1K_TOKENS = 0.00015
    CAPS_PER_AI_REQUEST = 5
    MAX_RAPID_MESSAGES = 6
    SPAM_BLOCK_DURATION_MINUTES = 30
    RAPID_THRESHOLD_SECONDS = 2
    STARTING_UID = 666
    MAX_UID = 99999
    # Admin secret — ТОЛЬКО из env var, без хардкожного default
    ADMIN_SECRET = os.environ.get('ADMIN_SECRET', '')


config = Config()
