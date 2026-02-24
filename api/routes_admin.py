#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Admin routes: migrations, shop CRUD, AI history, user chat, unblock
"""

import os
import time
import logging
import requests as http_requests
from flask import Blueprint, request, jsonify
from .auth import require_admin_secret
from .database import get_db
from .utils import send_telegram_message, log_balance_operation
from .database import get_setting
from .ai import check_achievements
from .config import config

logger = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/api/health', methods=['GET'])
def api_health():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM users")
        count = cur.fetchone()['cnt']
        conn.close()
        return jsonify({"status": "ok", "users": count, "database": "connected", "version": "2.1-security-modular"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@admin_bp.route('/api/migrate', methods=['GET'])
@require_admin_secret
def run_migration():
    try:
        conn = get_db()
        cur = conn.cursor()
        migrations = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS user_level TEXT DEFAULT 'basic'",
            """CREATE TABLE IF NOT EXISTS admin_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS admin_messages (id SERIAL PRIMARY KEY, user_telegram_id TEXT NOT NULL, direction TEXT NOT NULL, message TEXT NOT NULL, admin_username TEXT, created_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS admin_audit_log (id SERIAL PRIMARY KEY, admin_username TEXT NOT NULL, action TEXT NOT NULL, details TEXT, target_id TEXT, created_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS broadcast_history (id SERIAL PRIMARY KEY, message TEXT NOT NULL, photo_url TEXT, total_sent INTEGER DEFAULT 0, total_delivered INTEGER DEFAULT 0, total_failed INTEGER DEFAULT 0, admin_username TEXT, created_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS ai_knowledge_base (id SERIAL PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, file_type TEXT DEFAULT 'txt', priority INTEGER DEFAULT 1, is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS ai_learned_facts (id SERIAL PRIMARY KEY, question TEXT NOT NULL, answer TEXT NOT NULL, source TEXT DEFAULT 'user_interaction', priority INTEGER DEFAULT 1, created_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS ai_usage_log (id SERIAL PRIMARY KEY, user_id INTEGER, tokens_in INTEGER DEFAULT 0, tokens_out INTEGER DEFAULT 0, cost REAL DEFAULT 0.0, created_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS user_cart (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, item_id INTEGER NOT NULL, added_at TIMESTAMPTZ DEFAULT NOW(), UNIQUE(user_id, item_id))""",
            """CREATE TABLE IF NOT EXISTS lead_cards (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, telegram_id TEXT, field_name TEXT NOT NULL, field_value TEXT, collected_at TIMESTAMPTZ DEFAULT NOW(), UNIQUE(user_id, field_name))""",
            "ALTER TABLE shop_items ADD COLUMN IF NOT EXISTS file_url TEXT",
            "ALTER TABLE shop_items ADD COLUMN IF NOT EXISTS file_type TEXT",
            """CREATE TABLE IF NOT EXISTS shop_purchases (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, item_id INTEGER NOT NULL, price_paid INTEGER NOT NULL, purchased_at TIMESTAMPTZ DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS shop_items (id SERIAL PRIMARY KEY, category TEXT NOT NULL, title TEXT NOT NULL, description TEXT, price_caps INTEGER NOT NULL, content_text TEXT, file_url TEXT, file_type TEXT, is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMPTZ DEFAULT NOW())""",
            "ALTER TABLE ai_learned_facts ADD COLUMN IF NOT EXISTS fact TEXT",
            "ALTER TABLE ai_learned_facts ADD COLUMN IF NOT EXISTS confidence REAL DEFAULT 0.5",
            "ALTER TABLE ai_learned_facts ADD COLUMN IF NOT EXISTS learned_at TIMESTAMPTZ DEFAULT NOW()",
            """CREATE TABLE IF NOT EXISTS balance_history (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, amount INTEGER NOT NULL, operation TEXT NOT NULL, description TEXT, balance_after INTEGER, created_at TIMESTAMPTZ DEFAULT NOW())""",
        ]
        results = []
        for sql in migrations:
            try:
                cur.execute(sql)
                conn.commit()
                results.append(f"OK: {sql[:60]}...")
            except Exception as e:
                conn.rollback()
                results.append(f"ERR: {sql[:60]}... - {str(e)}")
        conn.close()
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/migrate-rls', methods=['POST'])
@require_admin_secret
def migrate_rls():
    """Execute RLS migration from sql file"""
    try:
        # Read migration SQL
        migration_path = os.path.join(os.path.dirname(__file__), 'migrations', 'enable_rls.sql')
        with open(migration_path, 'r') as f:
            sql = f.read()
        conn = get_db()
        cur = conn.cursor()
        # Execute each statement separately
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        results = []
        for stmt in statements:
            try:
                cur.execute(stmt)
                conn.commit()
                results.append(f"OK: {stmt[:80]}...")
            except Exception as e:
                conn.rollback()
                results.append(f"ERR: {stmt[:80]}... - {str(e)}")
        conn.close()
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/migrate-lessons', methods=['POST'])
@require_admin_secret
def migrate_lessons():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM university_lessons")
        conn.commit()
        # Re-seed lessons via database module
        from .database import _seed_university_lessons
        _seed_university_lessons(cur)
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Lessons migrated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/migrate-shop', methods=['POST'])
@require_admin_secret
def migrate_shop():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("ALTER TABLE shop_items ADD COLUMN IF NOT EXISTS file_url TEXT")
        cur.execute("ALTER TABLE shop_items ADD COLUMN IF NOT EXISTS file_type TEXT")
        cur.execute("DELETE FROM shop_items")
        cur.execute("""
            INSERT INTO shop_items (category, title, description, price_caps, content_text, file_url, file_type, is_active) VALUES
            ('manuals', '📖 Базовый мануал по процессингу', 'Пошаговое руководство для новичков. Формат: PDF', 50, 'Базовый мануал по процессингу — скачайте файл после покупки.', 'test_manual.pdf', 'pdf', TRUE),
            ('private', '🔐 Приватная схема #1', 'Эксклюзивная схема заработка. Формат: TXT', 150, 'Приватная схема — скачайте файл после покупки.', 'test_scheme.txt', 'txt', TRUE),
            ('schemes', '💡 Доп. схема: Арбитраж', 'Схема арбитражного заработка. Формат: XLSX', 100, 'Арбитражная схема — скачайте файл после покупки.', 'test_arbitrage.xlsx', 'xlsx', TRUE),
            ('training', '🎓 Продвинутый курс', 'Углубленное обучение процессингу', 200, 'Скоро будет доступно', NULL, NULL, TRUE),
            ('contacts', '📞 Контакты площадок', 'Список проверенных площадок', 75, 'Скоро будет доступно', NULL, NULL, TRUE),
            ('tables', '📊 Полезная табличка: Ставки', 'Сравнительная таблица ставок', 30, 'Скоро будет доступно', NULL, NULL, TRUE)
        """)
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Shop migrated with file support"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/shop/add-item', methods=['POST'])
@require_admin_secret
def admin_add_shop_item():
    try:
        data = request.json
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop_items (category, title, description, price_caps, content_text, file_url, file_type, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE) RETURNING id
        """, (data.get('category', 'manuals'), data.get('title', ''), data.get('description', ''),
              data.get('price_caps', 0), data.get('content_text', ''), data.get('file_url'), data.get('file_type')))
        item_id = cur.fetchone()['id']
        conn.commit()
        conn.close()
        return jsonify({"success": True, "item_id": item_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/shop/items', methods=['GET'])
@require_admin_secret
def admin_list_shop_items():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM shop_items ORDER BY category, id")
        items = cur.fetchall()
        conn.close()
        return jsonify({"success": True, "items": [dict(i) for i in items]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/shop/update-item', methods=['POST'])
@require_admin_secret
def admin_update_shop_item():
    try:
        data = request.json
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE shop_items SET title=%s, description=%s, price_caps=%s,
            content_text=%s, file_url=%s, file_type=%s, category=%s, is_active=%s WHERE id=%s
        """, (data.get('title'), data.get('description'), data.get('price_caps'),
              data.get('content_text'), data.get('file_url'), data.get('file_type'),
              data.get('category'), data.get('is_active', True), data.get('id')))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@admin_bp.route('/api/admin/shop/delete-item', methods=['POST'])
@require_admin_secret
def admin_delete_shop_item():
    try:
        data = request.json
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM shop_items WHERE id = %s", (data.get('id'),))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# === AI History ===
@admin_bp.route('/api/admin/ai-history', methods=['GET'])
@require_admin_secret
def admin_ai_history_users():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.telegram_id, u.username, u.first_name,
                   COUNT(*) as message_count, MAX(ac.created_at) as last_message_at
            FROM ai_conversations ac JOIN users u ON ac.user_id = u.telegram_id
            GROUP BY u.telegram_id, u.username, u.first_name ORDER BY last_message_at DESC
        """)
        rows = cur.fetchall()
        conn.close()
        users = [{"user_id": r["telegram_id"], "username": r["username"], "first_name": r["first_name"],
                  "message_count": r["message_count"],
                  "last_message_at": str(r["last_message_at"]) if r["last_message_at"] else None} for r in rows]
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/api/admin/ai-history/<int:user_id>', methods=['GET'])
@require_admin_secret
def admin_ai_history_messages(user_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE telegram_id = %s", (str(user_id),))
        db_user = cur.fetchone()
        internal_id = db_user['id'] if db_user else user_id
        cur.execute("""
            SELECT id, message, response, caps_spent, tokens_used, cost_usd, created_at
            FROM ai_conversations WHERE user_id = %s ORDER BY created_at ASC
        """, (internal_id,))
        rows = cur.fetchall()
        conn.close()
        messages = []
        for r in rows:
            messages.append({"id": r["id"], "role": "user", "content": r["message"],
                           "created_at": str(r["created_at"]) if r["created_at"] else None})
            if r["response"]:
                messages.append({"id": r["id"], "role": "assistant", "content": r["response"],
                               "created_at": str(r["created_at"]) if r["created_at"] else None,
                               "caps_spent": float(r["caps_spent"]) if r["caps_spent"] else 0,
                               "tokens_used": r["tokens_used"] or 0,
                               "cost_usd": float(r["cost_usd"]) if r["cost_usd"] else 0})
        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === User Chat ===
@admin_bp.route('/api/admin/user-chat/users', methods=['GET'])
@require_admin_secret
def admin_user_chat_users():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT am.user_telegram_id, u.username, u.first_name,
                   COUNT(*) as total_messages,
                   SUM(CASE WHEN am.direction='user_to_admin' THEN 1 ELSE 0 END) as unread_count,
                   MAX(am.created_at) as last_message_at
            FROM admin_messages am LEFT JOIN users u ON am.user_telegram_id = u.telegram_id
            GROUP BY am.user_telegram_id, u.username, u.first_name ORDER BY last_message_at DESC
        """)
        rows = cur.fetchall()
        conn.close()
        users = [{"user_id": r["user_telegram_id"], "username": r["username"], "first_name": r["first_name"],
                  "total_messages": r["total_messages"], "unread_count": r["unread_count"],
                  "last_message_at": str(r["last_message_at"]) if r["last_message_at"] else None} for r in rows]
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/api/admin/user-chat/messages/<int:user_id>', methods=['GET'])
@require_admin_secret
def admin_user_chat_messages(user_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, direction, message, created_at FROM admin_messages WHERE user_telegram_id = %s ORDER BY created_at ASC", (str(user_id),))
        rows = cur.fetchall()
        conn.close()
        messages = [{"id": r["id"], "direction": "in" if r["direction"] == "user_to_admin" else "out",
                    "text": r["message"], "created_at": str(r["created_at"]) if r["created_at"] else None} for r in rows]
        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/api/admin/user-chat/send', methods=['POST'])
@require_admin_secret
def admin_user_chat_send():
    try:
        data = request.json
        user_id = data.get('user_id')
        text = data.get('text')
        if not user_id or not text:
            return jsonify({"error": "user_id and text required"}), 400
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO admin_messages (user_telegram_id, direction, message) VALUES (%s, 'admin_to_user', %s)", (str(user_id), text))
        conn.commit()
        conn.close()
        bot_token = config.TELEGRAM_BOT_TOKEN
        resp = http_requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json={'chat_id': user_id, 'text': text})
        return jsonify({"success": True, "telegram_response": resp.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/api/admin/ai/unblock', methods=['POST'])
@require_admin_secret
def admin_ai_unblock():
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"success": False, "error": "user_id required"}), 400
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"success": False, "error": "User not found"}), 404
        cur.execute("UPDATE user_ai_sessions SET is_blocked = FALSE, message_count = 0, block_expires_at = NULL WHERE user_id = %s", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"AI unblocked for user {user_id}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== USER LEVEL CHANGE =====

@admin_bp.route('/api/admin/user/<int:user_id>/level', methods=['POST'])
@require_admin_secret
def admin_change_level(user_id):
    """Change user level and trigger achievement check"""
    try:
        data = request.get_json() or {}
        level = data.get('level', 'basic')
        if level not in ('basic', 'vip'):
            return jsonify({"success": False, "error": "Invalid level"}), 400

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT telegram_id, first_name FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            conn.close()
            return jsonify({"success": False, "error": "User not found"}), 404

        cur.execute("UPDATE users SET user_level = %s WHERE id = %s", (level, user_id))
        conn.commit()
        conn.close()

        # Notify user
        if level == 'vip':
            send_telegram_message(user['telegram_id'], "👑 <b>Поздравляем! Вы получили VIP статус!</b>\n\n🎁 Бонусы VIP:\n• Безлимитный доступ к ИИ (без списания крышек)\n• Приоритетная поддержка\n\n🍺 Наслаждайтесь привилегиями!")
        else:
            send_telegram_message(user['telegram_id'], "ℹ️ Ваш статус изменён на <b>Basic</b>.")

        # Check achievements (VIP achievement etc)
        check_achievements(user_id)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ADMIN SETTINGS =====

@admin_bp.route('/api/admin/settings', methods=['GET'])
@require_admin_secret
def admin_get_settings():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT key, value FROM admin_settings")
        rows = cur.fetchall()
        conn.close()
        settings = {r['key']: r['value'] for r in rows}
        return jsonify({"success": True, "settings": settings})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route('/api/admin/settings', methods=['POST'])
@require_admin_secret
def admin_update_settings():
    try:
        data = request.json or {}
        allowed_keys = {'news_daily_cost', 'ai_message_cost'}
        conn = get_db()
        cur = conn.cursor()
        updated = []
        for key, value in data.items():
            if key in allowed_keys:
                cur.execute("""
                    INSERT INTO admin_settings (key, value, updated_at) VALUES (%s, %s, NOW())
                    ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
                """, (key, str(value)))
                updated.append(key)
        conn.commit()
        conn.close()
        return jsonify({"success": True, "updated": updated})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== NEWS ADMIN =====

@admin_bp.route('/api/admin/news/broadcast', methods=['POST'])
@require_admin_secret
def admin_news_broadcast():
    try:
        data = request.json or {}
        message = data.get('message', '')
        if not message:
            return jsonify({"success": False, "error": "message required"}), 400

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT telegram_id FROM news_subscriptions
            WHERE is_active = TRUE
        """)
        subscribers = cur.fetchall()
        conn.close()

        sent = 0
        failed = 0
        for sub in subscribers:
            try:
                result = send_telegram_message(sub['telegram_id'], message)
                if result and result.get('ok'):
                    sent += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
            time.sleep(0.1)  # 100ms delay

        return jsonify({"success": True, "sent": sent, "failed": failed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route('/api/admin/news/subscribers', methods=['GET'])
@require_admin_secret
def admin_news_subscribers():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT ns.telegram_id, ns.is_active, ns.subscribed_at, ns.expires_at,
                   u.first_name, u.username
            FROM news_subscriptions ns
            JOIN users u ON ns.user_id = u.id
            WHERE ns.is_active = TRUE
            ORDER BY ns.subscribed_at DESC
        """)
        rows = cur.fetchall()
        conn.close()
        subscribers = []
        for r in rows:
            subscribers.append({
                "telegram_id": r['telegram_id'],
                "first_name": r['first_name'],
                "username": r['username'],
                "subscribed_at": r['subscribed_at'].isoformat() if r['subscribed_at'] else None,
                "expires_at": r['expires_at'].isoformat() if r['expires_at'] else None
            })
        return jsonify({"success": True, "subscribers": subscribers, "total": len(subscribers)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route('/api/admin/news/charge-daily', methods=['POST'])
@require_admin_secret
def admin_news_charge_daily():
    """Daily cron: charge subscribers, deactivate those without balance"""
    try:
        daily_cost = int(get_setting('news_daily_cost', '10'))
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT ns.id, ns.user_id, ns.telegram_id, u.caps_balance
            FROM news_subscriptions ns
            JOIN users u ON ns.user_id = u.id
            WHERE ns.is_active = TRUE
        """)
        subs = cur.fetchall()
        
        charged = 0
        deactivated = 0
        for sub in subs:
            if sub['caps_balance'] >= daily_cost:
                cur.execute("UPDATE users SET caps_balance = caps_balance - %s, total_spent_caps = total_spent_caps + %s WHERE id = %s",
                           (daily_cost, daily_cost, sub['user_id']))
                cur.execute("SELECT caps_balance FROM users WHERE id = %s", (sub['user_id'],))
                new_bal = cur.fetchone()['caps_balance']
                log_balance_operation(sub['user_id'], -daily_cost, 'news_daily_charge', 'Ежедневная подписка на новости', new_bal, conn)
                charged += 1
            else:
                cur.execute("UPDATE news_subscriptions SET is_active = FALSE WHERE id = %s", (sub['id'],))
                # Notify user
                try:
                    send_telegram_message(sub['telegram_id'], 
                        "📰 Подписка на новости отключена — недостаточно крышек.\nПополните баланс и подпишитесь снова в разделе Новости.")
                except: pass
                deactivated += 1
        
        conn.commit()
        conn.close()
        return jsonify({"success": True, "charged": charged, "deactivated": deactivated, "daily_cost": daily_cost})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
