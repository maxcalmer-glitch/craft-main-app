#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Form submission routes: application, SOS, support, offers
"""

import json
import logging
from flask import Blueprint, request, jsonify
from .auth import require_telegram_auth, check_rate_limit
from .database import get_db
from .utils import get_user, send_to_admin_chat
from .security import sanitize_user_input
from .ai import check_achievements
from .config import config

logger = logging.getLogger(__name__)
forms_bp = Blueprint('forms', __name__)


@forms_bp.route('/api/application/submit', methods=['POST'])
@require_telegram_auth
def api_submit_application():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        form_data = data.get('form_data', {})
        if not telegram_id or not form_data:
            return jsonify({"success": False, "error": "Required fields missing"}), 400

        # Rate limit: 5 req/min для форм
        if not check_rate_limit(f'form:{telegram_id}', 5, 60):
            return jsonify({"success": False, "error": "Слишком много заявок. Подождите минуту."}), 429

        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        # Sanitize form data
        sanitized_form = {}
        for k, v in form_data.items():
            sanitized_form[sanitize_user_input(str(k), 100)] = sanitize_user_input(str(v), 1000)

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO applications (user_id, form_data) VALUES (%s, %s) RETURNING id", (user['id'], json.dumps(sanitized_form, ensure_ascii=False)))
        app_id = cur.fetchone()['id']
        conn.commit()
        conn.close()

        msg = f"📋 <b>НОВАЯ ЗАЯВКА</b>\n👤 {user['first_name']} {user.get('last_name','')}\n🆔 #{user['system_uid']}\n💬 @{user.get('username','N/A')}"

        if user.get('referrer_id'):
            conn2 = get_db()
            cur2 = conn2.cursor()
            cur2.execute("SELECT first_name, username, system_uid FROM users WHERE id = %s", (user['referrer_id'],))
            ref_user = cur2.fetchone()
            conn2.close()
            if ref_user:
                ref_display = f"@{ref_user['username']}" if ref_user.get('username') else ref_user['first_name']
                msg += f"\n🤝 <b>Привел:</b> {ref_display} (#{ref_user['system_uid']})"

        for k, v in sanitized_form.items():
            msg += f"\n• <b>{k}:</b> {v}"
        send_to_admin_chat(config.ADMIN_CHAT_APPLICATIONS, msg)

        return jsonify({"success": True, "application_id": app_id, "message": "Заявка отправлена!"})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to submit"}), 500


@forms_bp.route('/api/sos/submit', methods=['POST'])
@require_telegram_auth
def api_submit_sos():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        city = sanitize_user_input(data.get('city', ''), 200)
        contact = sanitize_user_input(data.get('contact', ''), 200)
        description = sanitize_user_input(data.get('description', ''), 2000)
        if not all([telegram_id, city, contact, description]):
            return jsonify({"success": False, "error": "All fields required"}), 400

        # Rate limit: 5 req/min
        if not check_rate_limit(f'form:{telegram_id}', 5, 60):
            return jsonify({"success": False, "error": "Подождите минуту."}), 429

        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO sos_requests (user_id, city, contact, description) VALUES (%s, %s, %s, %s) RETURNING id", (user['id'], city, contact, description))
        sos_id = cur.fetchone()['id']
        conn.commit()
        conn.close()

        msg = f"🆘 <b>SOS ЗАЯВКА</b>\n👤 {user['first_name']}\n🆔 #{user['system_uid']}\n🏙️ {city}\n📞 {contact}\n📝 {description}\n❗ СРОЧНОЕ РЕАГИРОВАНИЕ"
        send_to_admin_chat(config.ADMIN_CHAT_SOS, msg)

        check_achievements(user['id'])

        return jsonify({"success": True, "sos_id": sos_id, "message": "SOS заявка отправлена!"})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to submit SOS"}), 500


@forms_bp.route('/api/support/submit', methods=['POST'])
@require_telegram_auth
def api_submit_support():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        message = sanitize_user_input(data.get('message', ''), 2000)
        if not telegram_id or not message:
            return jsonify({"success": False, "error": "Required fields missing"}), 400

        # Rate limit: 5 req/min
        if not check_rate_limit(f'form:{telegram_id}', 5, 60):
            return jsonify({"success": False, "error": "Подождите минуту."}), 429

        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO support_tickets (user_id, message) VALUES (%s, %s) RETURNING id", (user['id'], message))
        ticket_id = cur.fetchone()['id']
        conn.commit()
        conn.close()

        msg = f"💬 <b>ТЕХПОДДЕРЖКА</b>\n👤 {user['first_name']}\n🆔 #{user['system_uid']}\n📝 {message}"
        send_to_admin_chat(config.ADMIN_CHAT_SUPPORT, msg)

        return jsonify({"success": True, "ticket_id": ticket_id, "message": "Обращение принято!"})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to submit"}), 500


@forms_bp.route('/api/offers', methods=['GET'])
def api_offers():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT category, description, rate_from, rate_to, is_active FROM offers WHERE is_active = TRUE ORDER BY id ASC")
        offers = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify({"success": True, "offers": offers})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to load offers"}), 500
