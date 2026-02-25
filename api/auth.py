#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Аутентификация и авторизация
"""

import hashlib
import hmac
import json
import logging
import time
import urllib.parse
from collections import defaultdict
from functools import wraps

from flask import request, jsonify
from .config import config

logger = logging.getLogger(__name__)

# ===============================
# RATE LIMITING
# ===============================
# NOTE: In-memory rate limiting. На Vercel serverless каждый instance имеет
# свой словарь — это ограничение. Для полноценного rate limiting нужен Redis.
_rate_limits = defaultdict(list)


def check_rate_limit(key, max_requests=60, window_seconds=60):
    """Проверка rate limit. Default: 60 req/min (global)"""
    now = time.time()
    _rate_limits[key] = [t for t in _rate_limits[key] if now - t < window_seconds]
    if len(_rate_limits[key]) >= max_requests:
        return False
    _rate_limits[key].append(now)
    return True


# ===============================
# TELEGRAM INIT DATA VALIDATION
# ===============================

def validate_telegram_init_data(init_data_str, bot_token):
    """Validate Telegram WebApp initData via HMAC-SHA256 + auth_date check"""
    if not init_data_str or not bot_token:
        return False
    try:
        data = dict(urllib.parse.parse_qsl(init_data_str))
        received_hash = data.pop('hash', '')
        if not received_hash:
            return False
        data_check_string = '\n'.join(f'{k}={v}' for k, v in sorted(data.items()))
        secret_key = hmac.new(b'WebAppData', bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calculated_hash, received_hash):
            return False
        # Проверка auth_date — отклонять если > 4 часов (14400 секунд)
        auth_date = int(data.get('auth_date', 0))
        if time.time() - auth_date > 14400:
            return False
        return True
    except Exception as e:
        logger.error(f"initData validation error: {e}")
        return False


# ===============================
# AUTH DECORATORS
# ===============================

def require_telegram_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json(silent=True) or {}
        init_data = data.get('init_data') or request.args.get('init_data', '')
        if not init_data:
            return jsonify({"error": "Authentication required"}), 401
        if not validate_telegram_init_data(init_data, config.TELEGRAM_BOT_TOKEN):
            return jsonify({"error": "Invalid authentication"}), 403
        # Extract user_id from initData and attach to request
        try:
            parsed = dict(urllib.parse.parse_qsl(init_data))
            user_json = parsed.get('user', '{}')
            user_obj = json.loads(user_json)
            request.telegram_user_id = str(user_obj.get('id', ''))
        except Exception:
            request.telegram_user_id = ''
        return f(*args, **kwargs)
    return decorated


def require_admin_secret(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # C-1: Secret ONLY from header. Query string kept ONLY for cron endpoints (charge-daily)
        is_cron_endpoint = request.path.endswith('/charge-daily')
        if is_cron_endpoint:
            # Cron job cannot set headers, so query string is allowed here
            secret = request.args.get('secret', '') or request.headers.get('X-Admin-Secret', '')
        else:
            secret = request.headers.get('X-Admin-Secret', '')
        admin_secret = config.ADMIN_SECRET
        if not admin_secret:
            return jsonify({"error": "Admin secret not configured"}), 500
        # H-1: Timing-safe comparison to prevent timing attacks
        if not hmac.compare_digest(secret.encode(), admin_secret.encode()):
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated
