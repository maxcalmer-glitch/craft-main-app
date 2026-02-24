#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Утилиты: Telegram messaging, balance operations
"""

import io
import logging
import requests as http_requests
from .config import config
from .database import get_db

logger = logging.getLogger(__name__)


def send_to_admin_chat(chat_id, message, parse_mode='HTML'):
    if not chat_id or not config.TELEGRAM_BOT_TOKEN:
        return False
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        resp = http_requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": parse_mode}, timeout=10)
        return resp.status_code == 200
    except:
        return False


def check_channel_subscription(user_id, channel_id):
    if not channel_id or not config.TELEGRAM_BOT_TOKEN:
        return {"subscribed": True, "status": "unknown"}
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getChatMember"
        resp = http_requests.post(url, json={"chat_id": channel_id, "user_id": user_id}, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            if result.get('ok'):
                status = result.get('result', {}).get('status', 'left')
                return {"subscribed": status in ['creator', 'administrator', 'member'], "status": status}
        return {"subscribed": False, "status": "error"}
    except:
        return {"subscribed": False, "status": "error"}


def send_telegram_message(chat_id, text, reply_markup=None):
    """Отправка сообщения через Telegram Bot API"""
    try:
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        if reply_markup:
            payload['reply_markup'] = reply_markup
        response = http_requests.post(
            f'https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage',
            json=payload,
            timeout=10
        )
        return response.json()
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return None


def send_telegram_message_bot(chat_id, text):
    """Simple message send without markup"""
    return send_telegram_message(chat_id, text)


def send_telegram_video(chat_id, video_url, caption=None):
    """Send video via Telegram Bot API"""
    try:
        payload = {'chat_id': chat_id, 'video': video_url}
        if caption:
            payload['caption'] = caption
        response = http_requests.post(
            f'https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendVideo',
            json=payload, timeout=30
        )
        return response.json()
    except Exception as e:
        logger.error(f"Send video error: {e}")
        return None


def send_file_to_user(chat_id, item):
    """Send purchased file to user via Telegram bot"""
    if not config.TELEGRAM_BOT_TOKEN:
        return False
    try:
        file_type = item.get('file_type', 'txt')
        content = item.get('content_text', 'Содержимое товара')
        title = item.get('title', 'Товар')
        if file_type == 'pdf':
            msg = f"📄 <b>{title}</b>\n\n{content}\n\n<i>Файл в формате PDF будет доступен в следующем обновлении.</i>"
            send_telegram_message(chat_id, msg)
        elif file_type in ('txt', 'xlsx', 'csv'):
            url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendDocument"
            file_content = content.encode('utf-8')
            filename = f"{title.replace(' ', '_')}.{file_type}"
            files = {'document': (filename, io.BytesIO(file_content), 'application/octet-stream')}
            data = {'chat_id': chat_id, 'caption': f'📦 {title}'}
            http_requests.post(url, data=data, files=files, timeout=30)
        else:
            send_telegram_message(chat_id, f"📦 <b>{title}</b>\n\n{content}")
        return True
    except Exception as e:
        logger.error(f"Send file error: {e}")
        return False


def log_balance_operation(user_id, amount, operation, description, balance_after, conn=None):
    """Log balance operation to history"""
    should_close = False
    if not conn:
        conn = get_db()
        should_close = True
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO balance_history (user_id, amount, operation, description, balance_after)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (user_id, amount, operation, description, balance_after))
        if should_close:
            conn.commit()
    except Exception as e:
        logger.error(f"Balance log error: {e}")
    finally:
        if should_close:
            conn.close()


def get_user(telegram_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.*, COUNT(r.id) as total_referrals_count, COALESCE(SUM(r.caps_earned), 0) as total_referral_caps
            FROM users u LEFT JOIN referrals r ON u.id = r.referrer_id
            WHERE u.telegram_id = %s GROUP BY u.id
        """, (telegram_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Get user failed: {e}")
        return None
