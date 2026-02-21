from http.server import BaseHTTPRequestHandler
import json
import requests
import psycopg2
import os
import urllib.parse

# Токен бота
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

# Supabase connection
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db():
    """Подключение к Supabase PostgreSQL"""
    return psycopg2.connect(DATABASE_URL)

def send_message(chat_id, text, reply_markup=None):
    """Отправка сообщения через Telegram Bot API"""
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    if reply_markup:
        payload['reply_markup'] = reply_markup
    
    response = requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        json=payload
    )
    return response.json()

def handle_start_command(chat_id, user_id, text, username=None, first_name=None):
    """Обработка команды /start"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Регистрация пользователя в БД если еще нет
        cur.execute(
            '''INSERT INTO users (telegram_id, username, first_name, caps_balance) 
               VALUES (%s, %s, %s, 100) 
               ON CONFLICT (telegram_id) DO NOTHING''',
            (user_id, username, first_name)
        )
        
        # Проверка реферального параметра
        referral_message = ""
        if 'ref_' in text:
            try:
                referrer_id = text.split('ref_')[1].strip()
                
                if referrer_id != user_id:  # Нельзя реферить самого себя
                    # Проверить что реферер существует
                    cur.execute('SELECT telegram_id FROM users WHERE telegram_id = %s', (referrer_id,))
                    if cur.fetchone():
                        # Сохранить реферальную связь
                        cur.execute(
                            '''INSERT INTO pending_referrals (referred_user_id, referrer_id) 
                               VALUES (%s, %s) 
                               ON CONFLICT DO NOTHING''',
                            (user_id, referrer_id)
                        )
                        
                        referral_message = f"\n\n🎉 Отлично! Вас пригласил пользователь #{referrer_id}!\nВы оба получите бонусы после регистрации в приложении!"
            except Exception as e:
                print(f"Referral processing error: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Создать WebApp кнопку
        keyboard = {
            'inline_keyboard': [[{
                'text': '🍺 Открыть CRAFT',
                'web_app': {'url': 'https://craft-main-app.vercel.app'}
            }]]
        }
        
        welcome_text = f"🍺 Добро пожаловать в CRAFT!{referral_message}\n\nНажмите кнопку чтобы открыть приложение:"
        
        send_message(chat_id, welcome_text, keyboard)
        
    except Exception as e:
        print(f"Start command error: {e}")
        send_message(chat_id, "❌ Произошла ошибка, попробуйте позже")

def handle_ref_command(chat_id, user_id):
    """Обработка команды /ref"""
    try:
        ref_link = f"https://t.me/CRAFT_hell_bot?start=ref_{user_id}"
        
        message = (
            f"🔗 *Ваша реферальная ссылка:*\n\n"
            f"`{ref_link}`\n\n"
            f"💰 *Система наград:*\n"
            f"• 1-й уровень: **30 крышек** за каждого друга\n"
            f"• 2-й уровень: **15 крышек** за друзей ваших друзей\n\n"
            f"🍺 Поделитесь ссылкой с друзьями и зарабатывайте!"
        )
        
        send_message(chat_id, message)
        
    except Exception as e:
        print(f"Ref command error: {e}")
        send_message(chat_id, "❌ Ошибка получения реферальной ссылки")

def handle_stats_command(chat_id, user_id):
    """Обработка команды /stats"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Получить статистику рефералов
        cur.execute(
            'SELECT COUNT(*) FROM referrals WHERE referrer_id = %s AND level = 1',
            (user_id,)
        )
        level1_count = cur.fetchone()[0]
        
        cur.execute(
            'SELECT COUNT(*) FROM referrals WHERE referrer_id = %s AND level = 2',
            (user_id,)
        )
        level2_count = cur.fetchone()[0]
        
        cur.execute(
            'SELECT COALESCE(SUM(bonus_amount), 0) FROM referrals WHERE referrer_id = %s',
            (user_id,)
        )
        total_earned = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        message = (
            f"📊 *Ваша реферальная статистика:*\n\n"
            f"👥 Рефералы 1-го уровня: **{level1_count}**\n"
            f"👥 Рефералы 2-го уровня: **{level2_count}**\n"
            f"💰 Заработано всего: **{total_earned} крышек**\n\n"
            f"🍺 Продолжайте приглашать друзей!"
        )
        
        send_message(chat_id, message)
        
    except Exception as e:
        print(f"Stats command error: {e}")
        send_message(chat_id, "❌ Ошибка получения статистики")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """GET запрос - статус webhook"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'CRAFT Bot Webhook',
            'version': 'v6.1',
            'ready': True
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """POST запрос - обработка webhook от Telegram"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data.decode('utf-8'))
            
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                user_id = str(message['from']['id'])
                username = message['from'].get('username')
                first_name = message['from'].get('first_name')
                text = message.get('text', '')
                
                if text.startswith('/start'):
                    handle_start_command(chat_id, user_id, text, username, first_name)
                elif text == '/ref':
                    handle_ref_command(chat_id, user_id)
                elif text == '/stats':
                    handle_stats_command(chat_id, user_id)
                else:
                    # Неизвестная команда
                    send_message(chat_id, "🤖 Доступные команды:\n/start - начать\n/ref - получить реферальную ссылку\n/stats - статистика рефералов")
            
            # Ответ Telegram
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'ok': True}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Webhook error: {e}")
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'ok': False, 'error': str(e)}
            self.wfile.write(json.dumps(response).encode())