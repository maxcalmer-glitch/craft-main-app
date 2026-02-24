#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — University & Achievements routes
"""

import logging
from flask import Blueprint, request, jsonify
from .auth import require_telegram_auth
from .database import get_db
from .utils import get_user, log_balance_operation
from .ai import check_achievements

logger = logging.getLogger(__name__)
university_bp = Blueprint('university', __name__)


@university_bp.route('/api/university/lessons', methods=['GET'])
@require_telegram_auth
def api_university_lessons():
    try:
        user = get_user(request.telegram_user_id or request.args.get('telegram_id', ''))
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, exam_questions, reward_caps, order_index FROM university_lessons WHERE is_active = TRUE ORDER BY order_index ASC")
        lessons = [dict(r) for r in cur.fetchall()]
        if user:
            cur.execute("SELECT lesson_id, completed, score FROM university_progress WHERE user_id = %s", (user['id'],))
            progress = {r['lesson_id']: {'completed': r['completed'], 'score': r['score']} for r in cur.fetchall()}
            for l in lessons:
                p = progress.get(l['id'], {})
                l['completed'] = p.get('completed', False)
                l['score'] = p.get('score', 0)
        conn.close()
        return jsonify({"success": True, "lessons": lessons})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to load lessons"}), 500


@university_bp.route('/api/university/complete', methods=['POST'])
@require_telegram_auth
def api_university_complete():
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id', '')
        lesson_id = data.get('lesson_id')
        score = data.get('score', 0)
        total = data.get('total', 0)
        if not telegram_id or not lesson_id:
            return jsonify({"success": False, "error": "lesson_id required"}), 400
        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, reward_caps FROM university_lessons WHERE id = %s AND is_active = TRUE", (lesson_id,))
        lesson = cur.fetchone()
        if not lesson:
            conn.close()
            return jsonify({"success": False, "error": "Lesson not found"}), 404
        cur.execute("SELECT completed FROM university_progress WHERE user_id = %s AND lesson_id = %s", (user['id'], lesson_id))
        existing = cur.fetchone()
        if existing and existing['completed']:
            conn.close()
            return jsonify({"success": True, "already_completed": True, "message": "Урок уже пройден!"})
        if total > 0 and score < total:
            conn.close()
            return jsonify({"success": False, "error": f"Ответьте правильно на все вопросы ({score}/{total})"})
        cur.execute("""
            INSERT INTO university_progress (user_id, lesson_id, completed, score, attempts, completed_at)
            VALUES (%s, %s, TRUE, %s, 1, NOW())
            ON CONFLICT (user_id, lesson_id) DO UPDATE SET completed = TRUE, score = %s, attempts = university_progress.attempts + 1, completed_at = NOW()
        """, (user['id'], lesson_id, score, score))
        reward = lesson['reward_caps'] or 0
        if reward > 0 and not (existing and existing['completed']):
            cur.execute("UPDATE users SET caps_balance = caps_balance + %s, total_earned_caps = total_earned_caps + %s WHERE id = %s", (reward, reward, user['id']))
            cur.execute("SELECT caps_balance FROM users WHERE id = %s", (user['id'],))
            bal = cur.fetchone()
            log_balance_operation(user['id'], reward, 'lesson_reward', f'Урок пройден: #{lesson_id}', bal['caps_balance'] if bal else 0, conn)
        conn.commit()
        conn.close()
        try:
            check_achievements(user['id'])
        except Exception:
            pass
        return jsonify({"success": True, "reward": reward, "message": "Урок пройден! 🎓✅"})
    except Exception as e:
        logger.error(f"University complete error: {e}")
        return jsonify({"success": False, "error": "Ошибка сохранения"}), 500


@university_bp.route('/api/achievements/all', methods=['GET'])
@require_telegram_auth
def api_achievements_all():
    try:
        telegram_id = request.args.get('telegram_id', '')
        if not telegram_id:
            return jsonify({"success": False, "error": "Telegram ID required"}), 400
        user = get_user(telegram_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, a.code, a.name, a.description, a.icon, a.reward_caps,
                   CASE WHEN ua.id IS NOT NULL THEN TRUE ELSE FALSE END as earned
            FROM achievements a
            LEFT JOIN user_achievements ua ON a.id = ua.achievement_id AND ua.user_id = %s
            WHERE a.is_active = TRUE ORDER BY a.id
        """, (user['id'],))
        achievements = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify({"success": True, "achievements": achievements})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
