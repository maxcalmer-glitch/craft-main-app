#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Shop routes
"""

import logging
from flask import Blueprint, request, jsonify
from .auth import require_telegram_auth
from .database import get_db
from .utils import get_user, log_balance_operation, send_telegram_message, send_file_to_user
from .ai import check_achievements

logger = logging.getLogger(__name__)
shop_bp = Blueprint('shop', __name__)


@shop_bp.route('/api/shop/items', methods=['GET'])
@require_telegram_auth
def api_shop_items():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, category, title, description, price_caps, file_url, file_type FROM shop_items WHERE is_active = TRUE ORDER BY category, id")
        items = [dict(r) for r in cur.fetchall()]
        conn.close()
        grouped = {}
        for item in items:
            cat = item['category']
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(item)
        return jsonify({"success": True, "items": grouped})
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@shop_bp.route('/api/shop/cart/add', methods=['POST'])
@require_telegram_auth
def api_shop_cart_add():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        if not item_id:
            return jsonify({"success": False, "error": "item_id required"}), 400
        user = get_user(request.telegram_user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM shop_items WHERE id = %s AND is_active = TRUE", (item_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"success": False, "error": "Item not found"}), 404
        cur.execute("INSERT INTO user_cart (user_id, item_id) VALUES (%s, %s) ON CONFLICT (user_id, item_id) DO NOTHING", (user['id'], item_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@shop_bp.route('/api/shop/cart/remove', methods=['POST'])
@require_telegram_auth
def api_shop_cart_remove():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        if not item_id:
            return jsonify({"success": False, "error": "item_id required"}), 400
        user = get_user(request.telegram_user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM user_cart WHERE user_id = %s AND item_id = %s", (user['id'], item_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@shop_bp.route('/api/shop/cart', methods=['GET'])
@require_telegram_auth
def api_shop_cart():
    try:
        user = get_user(request.telegram_user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, s.title, s.description, s.price_caps, s.category
            FROM user_cart c JOIN shop_items s ON c.item_id = s.id
            WHERE c.user_id = %s ORDER BY c.added_at
        """, (user['id'],))
        items = [dict(r) for r in cur.fetchall()]
        total = sum(i['price_caps'] for i in items)
        conn.close()
        return jsonify({"success": True, "items": items, "total": total})
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@shop_bp.route('/api/shop/checkout', methods=['POST'])
@require_telegram_auth
def api_shop_checkout():
    try:
        user = get_user(request.telegram_user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, s.price_caps FROM user_cart c JOIN shop_items s ON c.item_id = s.id
            WHERE c.user_id = %s
        """, (user['id'],))
        cart_items = cur.fetchall()
        if not cart_items:
            conn.close()
            return jsonify({"success": False, "error": "Корзина пуста"}), 400
        total = sum(i['price_caps'] for i in cart_items)
        if user['caps_balance'] < total:
            conn.close()
            return jsonify({"success": False, "error": f"Недостаточно крышек. Нужно: {total}, у вас: {user['caps_balance']}"}), 400

        purchased_items = []
        for ci in cart_items:
            cur.execute("SELECT * FROM shop_items WHERE id = %s", (ci['id'],))
            full_item = cur.fetchone()
            if full_item:
                purchased_items.append(dict(full_item))

        cur.execute("UPDATE users SET caps_balance = caps_balance - %s, total_spent_caps = total_spent_caps + %s WHERE id = %s", (total, total, user['id']))
        new_balance = user['caps_balance'] - total
        log_balance_operation(user['id'], -total, 'shop_purchase', f'Покупка: {", ".join([pi["title"] for pi in purchased_items])}', new_balance, conn)

        for item in cart_items:
            cur.execute("INSERT INTO shop_purchases (user_id, item_id, price_paid) VALUES (%s, %s, %s)", (user['id'], item['id'], item['price_caps']))

        cur.execute("DELETE FROM user_cart WHERE user_id = %s", (user['id'],))

        # Referral commissions
        try:
            cur.execute("SELECT referrer_id FROM users WHERE id = %s", (user['id'],))
            ref_row = cur.fetchone()
            if ref_row and ref_row['referrer_id']:
                l1_id = ref_row['referrer_id']
                l1_bonus = max(1, int(total * 0.05))
                cur.execute("UPDATE users SET caps_balance = caps_balance + %s, total_earned_caps = total_earned_caps + %s WHERE id = %s", (l1_bonus, l1_bonus, l1_id))
                cur.execute("SELECT caps_balance, telegram_id, first_name FROM users WHERE id = %s", (l1_id,))
                l1_user = cur.fetchone()
                log_balance_operation(l1_id, l1_bonus, 'referral_purchase', f'5% от покупки реферала (#{user["id"]}): {total} крышек', l1_user['caps_balance'] if l1_user else 0, conn)
                if l1_user and l1_user.get('telegram_id'):
                    try:
                        send_telegram_message(int(l1_user['telegram_id']),
                            f"💰 <b>Реферальный бонус!</b>\n\nВаш реферал совершил покупку на {total} 🍺\nВы получили <b>+{l1_bonus} крышек</b> (5%)")
                    except: pass

                cur.execute("SELECT referrer_id FROM users WHERE id = %s", (l1_id,))
                l2_row = cur.fetchone()
                if l2_row and l2_row['referrer_id']:
                    l2_id = l2_row['referrer_id']
                    l2_bonus = max(1, int(total * 0.02))
                    cur.execute("UPDATE users SET caps_balance = caps_balance + %s, total_earned_caps = total_earned_caps + %s WHERE id = %s", (l2_bonus, l2_bonus, l2_id))
                    cur.execute("SELECT caps_balance FROM users WHERE id = %s", (l2_id,))
                    l2_user = cur.fetchone()
                    log_balance_operation(l2_id, l2_bonus, 'referral_purchase', f'2% от покупки реферала L2 (#{user["id"]}): {total} крышек', l2_user['caps_balance'] if l2_user else 0, conn)
        except Exception as e:
            logger.error(f"Referral commission error: {e}")

        cur.execute("SELECT telegram_id FROM users WHERE id = %s", (user['id'],))
        user_data = cur.fetchone()
        conn.commit()
        conn.close()

        # Send purchased content via Telegram
        for pi in purchased_items:
            telegram_id = user_data.get('telegram_id', '') if user_data else ''
            if telegram_id and telegram_id != 'SYSTEM':
                try:
                    if pi.get('file_url') and pi.get('file_type'):
                        file_msg = f"🛒 <b>Спасибо за покупку!</b>\n\n📦 <b>{pi['title']}</b>\n\nВаш товар отправлен ниже 👇"
                        send_telegram_message(int(telegram_id), file_msg)
                        send_file_to_user(int(telegram_id), pi)
                    elif pi.get('content_text'):
                        msg = f"🛒 <b>Спасибо за покупку!</b>\n\n📦 <b>{pi['title']}</b>\n\n{pi['content_text']}"
                        send_telegram_message(int(telegram_id), msg)
                    else:
                        msg = f"🛒 <b>Покупка оформлена!</b>\n\n📦 <b>{pi['title']}</b>\n\n<i>Товар будет доступен в ближайшее время.</i>"
                        send_telegram_message(int(telegram_id), msg)
                except Exception as e:
                    logger.error(f"File delivery error: {e}")

        try:
            check_achievements(user['id'])
        except Exception:
            pass
        return jsonify({"success": True, "total_spent": total, "new_balance": user['caps_balance'] - total})
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@shop_bp.route('/api/shop/purchases', methods=['GET'])
@require_telegram_auth
def api_shop_purchases():
    try:
        user = get_user(request.telegram_user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.title, s.category, p.price_paid, p.purchased_at
            FROM shop_purchases p JOIN shop_items s ON p.item_id = s.id
            WHERE p.user_id = %s ORDER BY p.purchased_at DESC
        """, (user['id'],))
        purchases = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify({"success": True, "purchases": purchases})
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500
