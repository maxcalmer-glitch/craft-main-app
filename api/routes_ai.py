#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — AI Chat routes
"""

import logging
from flask import Blueprint, request, jsonify
from .auth import require_telegram_auth, check_rate_limit
from .utils import get_user
from .ai import get_ai_response

logger = logging.getLogger(__name__)
ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/api/ai/chat', methods=['POST'])
@require_telegram_auth
def api_ai_chat():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        message = data.get('message', '').strip()
        if not telegram_id or not message:
            return jsonify({"success": False, "error": "Telegram ID and message required"}), 400
        # Rate limit: 10 req/min для AI endpoint
        if not check_rate_limit(f'ai:{telegram_id}', 10, 60):
            return jsonify({"success": False, "error": "Слишком много запросов. Подождите минуту."}), 429
        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        result = get_ai_response(user['id'], message, telegram_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"AI chat failed: {e}")
        return jsonify({"success": False, "error": "AI chat temporarily unavailable"}), 500
