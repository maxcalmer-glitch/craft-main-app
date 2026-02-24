#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Telegram Bot webhook routes
"""

import os
import logging
import requests as http_requests
from flask import Blueprint, request, jsonify
from .auth import require_admin_secret
from .database import get_db
from .utils import get_user, send_telegram_message
from .config import config

logger = logging.getLogger(__name__)
bot_bp = Blueprint('bot', __name__)


def handle_bot_start_command(chat_id, user_id, text, username=None, first_name=None):
    """Обработка команды /start от бота"""
    try:
        is_referral = False
        referrer_name = ""
        if 'ref_' in text:
            try:
                referrer_id = text.split('ref_')[1].strip()
                if referrer_id and referrer_id != user_id:
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM pending_referrals WHERE referred_user_id = %s AND referrer_id = %s", (str(user_id), str(referrer_id)))
                    already_pending = cur.fetchone()
                    cur.execute("SELECT id FROM referrals WHERE referred_id = %s", (str(user_id),))
                    already_referred = cur.fetchone()

                    if not already_pending and not already_referred:
                        cur.execute(
                            '''INSERT INTO pending_referrals (referred_user_id, referrer_id, processed)
                               VALUES (%s, %s, FALSE)
                               ON CONFLICT (referred_user_id, referrer_id) DO NOTHING''',
                            (str(user_id), str(referrer_id))
                        )
                        conn.commit()
                        referrer = get_user(str(referrer_id))
                        if referrer:
                            referrer_name = referrer.get('first_name') or referrer.get('username') or f"#{referrer['system_uid']}"
                            send_telegram_message(
                                referrer_id,
                                f"🎉 <b>У вас новый реферал!</b>\n\n"
                                f"👤 <b>{first_name or username or 'Пользователь'}</b> перешел по вашей ссылке\n"
                                f"⏳ Осталось только зарегистрироваться в приложении\n\n"
                                f"💰 После регистрации вы получите <b>+30 крышек</b>!"
                            )
                        else:
                            referrer_name = f"#{referrer_id}"
                    else:
                        referrer = get_user(str(referrer_id))
                        if referrer:
                            referrer_name = referrer.get('first_name') or referrer.get('username') or f"#{referrer['system_uid']}"
                        else:
                            referrer_name = f"#{referrer_id}"
                    conn.close()
                    is_referral = True
            except Exception as e:
                logger.error(f"Referral processing error: {e}")

        keyboard = {
            'inline_keyboard': [[{
                'text': '🍺 Открыть CRAFT',
                'web_app': {'url': config.APP_URL}
            }]]
        }

        base_welcome = (
            "🍺 <b>Добро пожаловать в CRAFT!</b>\n\n"
            "CRAFT — платформа для обучения, ведения и сопровождения команд в мире процессинга.\n\n"
            "🧠 Наш ИИ-помощник Михалыч — 3 года опыта работы командой, отлично знает рынок процессинга изнутри.\n\n"
            "🎓 <b>Университет CRAFT:</b>\n"
            "• Откроет двери в мир заработка на процессинге\n"
            "• Научит работать безопасно и максимально выгодно\n"
            "• Подскажет, куда развиваться после процессинга\n\n"
            "🍻 <b>Что внутри:</b>\n"
            "• Обучение от базы до продвинутого уровня\n"
            "• ИИ-консультант 24/7\n"
            "• Магазин мануалов и схем\n"
            "• Реферальная программа\n\n"
            "🚀 <b>Нажмите кнопку, чтобы открыть приложение!</b>"
        )
        if is_referral:
            welcome_text = (
                f"🎉 Вас пригласил <b>{referrer_name}</b>!\n\n"
                + base_welcome + "\n\n"
                "🎁 <b>Бонусы за реферал:</b>\n"
                "• <b>+50 крышек</b> за переход по ссылке друга"
            )
        else:
            welcome_text = base_welcome

        send_telegram_message(chat_id, welcome_text, keyboard)
    except Exception as e:
        logger.error(f"Start command error: {e}")
        send_telegram_message(chat_id, "❌ Произошла ошибка, попробуйте позже")


def handle_bot_ref_command(chat_id, user_id):
    try:
        user = get_user(user_id)
        if not user:
            send_telegram_message(chat_id, "❌ Пользователь не найден")
            return
        ref_link = f"https://t.me/CRAFT_hell_bot?start=ref_{user_id}"
        message = (
            f"🔗 <b>Ваша реферальная ссылка:</b>\n\n"
            f"<code>{ref_link}</code>\n\n"
            f"💰 <b>Система наград:</b>\n"
            f"• Вы: <b>+30 крышек</b> за каждого друга\n"
            f"• Ваш друг: <b>+50 крышек</b> бонус за переход\n"
            f"• Друзья друзей: <b>+15 крышек</b> дополнительно\n\n"
            f"🍺 Поделитесь ссылкой с друзьями и зарабатывайте!"
        )
        send_telegram_message(chat_id, message)
    except Exception as e:
        logger.error(f"Ref command error: {e}")
        send_telegram_message(chat_id, "❌ Ошибка получения реферальной ссылки")


def handle_bot_stats_command(chat_id, user_id):
    try:
        user = get_user(user_id)
        if not user:
            send_telegram_message(chat_id, "❌ Пользователь не найден")
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) as cnt FROM referrals WHERE referrer_id = %s AND level = 1', (user['id'],))
        level1_count = cur.fetchone()['cnt']
        cur.execute('SELECT COUNT(*) as cnt FROM referrals WHERE referrer_id = %s AND level = 2', (user['id'],))
        level2_count = cur.fetchone()['cnt']
        cur.execute('SELECT COALESCE(SUM(caps_earned), 0) as total FROM referrals WHERE referrer_id = %s', (user['id'],))
        total_earned = cur.fetchone()['total']
        conn.close()
        message = (
            f"📊 <b>Ваша реферальная статистика:</b>\n\n"
            f"👥 Рефералы 1-го уровня: <b>{level1_count}</b>\n"
            f"👥 Рефералы 2-го уровня: <b>{level2_count}</b>\n"
            f"💰 Заработано всего: <b>{total_earned} крышек</b>\n\n"
            f"🍺 Продолжайте приглашать друзей!"
        )
        send_telegram_message(chat_id, message)
    except Exception as e:
        logger.error(f"Stats command error: {e}")
        send_telegram_message(chat_id, "❌ Ошибка получения статистики")


@bot_bp.route('/api/bot/webhook', methods=['GET', 'POST'])
def bot_webhook():
    if request.method == 'GET':
        return jsonify({'status': 'CRAFT Bot Webhook', 'version': 'v6.2', 'ready': True, 'endpoint': '/api/bot/webhook'})

    try:
        update = request.get_json()
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = str(message['from']['id'])
            username = message['from'].get('username')
            first_name = message['from'].get('first_name')
            text = message.get('text', '')

            if text.startswith('/start'):
                handle_bot_start_command(chat_id, user_id, text, username, first_name)
            elif text == '/ref':
                handle_bot_ref_command(chat_id, user_id)
            elif text == '/stats':
                handle_bot_stats_command(chat_id, user_id)
            elif text.startswith('/'):
                send_telegram_message(chat_id, "🤖 Доступные команды:\n/start - начать\n/ref - получить реферальную ссылку\n/stats - статистика рефералов")
            else:
                try:
                    conn2 = get_db()
                    cur2 = conn2.cursor()
                    cur2.execute(
                        "INSERT INTO admin_messages (user_telegram_id, direction, message) VALUES (%s, 'user_to_admin', %s)",
                        (user_id, text[:2000])
                    )
                    conn2.commit()
                    conn2.close()
                except Exception as e:
                    logger.error(f"Failed to save user message: {e}")

                keyboard = {
                    'inline_keyboard': [[{
                        'text': '🍺 Открыть CRAFT',
                        'web_app': {'url': config.APP_URL}
                    }]]
                }
                send_telegram_message(chat_id, "💬 Ваше сообщение получено! Администратор скоро ответит.\n\n🍺 Или откройте приложение:", keyboard)

        return jsonify({'ok': True})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500


@bot_bp.route('/api/bot/set-webhook', methods=['GET'])
@require_admin_secret
def set_webhook():
    webhook_url = f"{config.APP_URL}/api/bot/webhook"
    resp = http_requests.post(
        f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/setWebhook",
        json={"url": webhook_url, "allowed_updates": ["message"]},
        timeout=10
    )
    return jsonify(resp.json())


@bot_bp.route('/api/bot/webhook-info', methods=['GET'])
@require_admin_secret
def webhook_info():
    resp = http_requests.get(
        f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getWebhookInfo",
        timeout=10
    )
    return jsonify(resp.json())
