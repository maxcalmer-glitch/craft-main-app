#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — User routes: init, profile, referral, balance, subscription
"""

import logging
from flask import Blueprint, request, jsonify
from .auth import require_telegram_auth
from .database import get_db
from .utils import get_user, check_channel_subscription
from .ai import create_user, check_achievements
from .config import config

logger = logging.getLogger(__name__)
user_bp = Blueprint('user', __name__)


@user_bp.route('/api/init', methods=['POST'])
@require_telegram_auth
def api_init():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        if not telegram_id:
            return jsonify({"success": False, "error": "Telegram ID required"}), 400

        user = get_user(telegram_id)
        if user:
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute("UPDATE users SET last_activity = NOW() WHERE telegram_id = %s", (telegram_id,))
                conn.commit()
                conn.close()
            except: pass

            try: check_achievements(user['id'])
            except: pass

            return jsonify({
                "success": True, "system_uid": user['system_uid'],
                "caps_balance": user['caps_balance'],
                "total_referrals": user.get('total_referrals_count', 0), "exists": True
            })

        result = create_user(
            telegram_id=telegram_id, first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''), username=data.get('username', ''),
            referrer_uid=data.get('referrer_uid'))

        if result["success"]:
            return jsonify({"success": True, "system_uid": result['system_uid'], "caps_balance": result['caps_balance'], "total_referrals": 0, "exists": False})
        return jsonify(result), 400
    except Exception as e:
        logger.error(f"API init failed: {e}")
        return jsonify({"success": False, "error": "Initialization failed"}), 500


@user_bp.route('/api/user/profile', methods=['GET'])
@require_telegram_auth
def api_user_profile():
    try:
        telegram_id = request.args.get('telegram_id', '')
        if not telegram_id:
            return jsonify({"success": False, "error": "Telegram ID required"}), 400
        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT level, COUNT(*) as count, SUM(caps_earned) as caps_earned FROM referrals WHERE referrer_id = %s GROUP BY level", (user['id'],))
        referrals_data = {}
        for r in cur.fetchall():
            referrals_data[f"level_{r['level']}"] = {"count": r['count'], "caps_earned": r['caps_earned'] or 0}

        cur.execute("""
            SELECT a.code, a.name, a.icon, a.reward_caps, ua.earned_at
            FROM user_achievements ua JOIN achievements a ON ua.achievement_id = a.id
            WHERE ua.user_id = %s ORDER BY ua.earned_at DESC
        """, (user['id'],))
        achievements = [dict(r) for r in cur.fetchall()]

        conn.close()

        return jsonify({"success": True, "profile": {
            "system_uid": user['system_uid'], "first_name": user['first_name'],
            "last_name": user['last_name'], "username": user['username'],
            "caps_balance": user['caps_balance'], "total_earned_caps": user['total_earned_caps'],
            "total_spent_caps": user['total_spent_caps'], "ai_requests_count": user['ai_requests_count'],
            "created_at": str(user['created_at']), "referrals": referrals_data, "achievements": achievements,
            "user_level": user.get('user_level', 'basic')
        }})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to load profile"}), 500


@user_bp.route('/api/referral/stats', methods=['GET'])
@require_telegram_auth
def api_referral_stats():
    try:
        telegram_id = request.args.get('telegram_id', '')
        if not telegram_id:
            return jsonify({"success": False, "error": "Telegram ID required"}), 400
        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) as cnt FROM referrals WHERE referrer_id = %s AND level = 1", (user['id'],))
        l1 = cur.fetchone()['cnt']
        cur.execute("SELECT COUNT(*) as cnt FROM referrals WHERE referrer_id = %s AND level = 2", (user['id'],))
        l2 = cur.fetchone()['cnt']
        cur.execute("SELECT COALESCE(SUM(caps_earned), 0) as total FROM referrals WHERE referrer_id = %s", (user['id'],))
        total = cur.fetchone()['total']

        cur.execute("""
            SELECT u.first_name, u.username, r.created_at
            FROM referrals r JOIN users u ON r.referred_id = u.id
            WHERE r.referrer_id = %s ORDER BY r.created_at DESC LIMIT 5
        """, (user['id'],))
        recent = [{"name": (r['first_name'] or '') + (' @'+r['username'] if r['username'] else ''), "date": r['created_at'].strftime('%d.%m.%Y') if r['created_at'] else ''} for r in cur.fetchall()]

        conn.close()
        return jsonify({"success": True, "stats": {"level1_count": l1, "level2_count": l2, "total_earned": total, "recent": recent}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_bp.route('/api/balance/history', methods=['GET'])
@require_telegram_auth
def api_balance_history():
    try:
        user = get_user(request.telegram_user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        filter_type = request.args.get('filter', 'all')
        conn = get_db()
        cur = conn.cursor()
        query = "SELECT * FROM balance_history WHERE user_id = %s"
        params = [user['id']]
        if filter_type == 'income':
            query += " AND amount > 0"
        elif filter_type == 'expense':
            query += " AND amount < 0"
        query += " ORDER BY created_at DESC LIMIT 50"
        cur.execute(query, params)
        history = [dict(r) for r in cur.fetchall()]
        conn.close()
        for h in history:
            if h.get('created_at'):
                h['created_at'] = h['created_at'].isoformat()
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_bp.route('/api/check-subscription', methods=['POST'])
@require_telegram_auth
def api_check_subscription():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        if not telegram_id:
            return jsonify({"success": False, "error": "Telegram ID required"}), 400
        result = check_channel_subscription(telegram_id, config.REQUIRED_CHANNEL_ID)
        return jsonify({"success": True, **result, "channel_id": config.REQUIRED_CHANNEL_ID})
    except Exception as e:
        return jsonify({"success": False, "error": "Subscription check failed"}), 500
