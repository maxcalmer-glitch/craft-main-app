#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — База данных (PostgreSQL/Supabase)
"""

import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import config

logger = logging.getLogger(__name__)


def get_db():
    """Get PostgreSQL connection"""
    conn = psycopg2.connect(config.DATABASE_URL, cursor_factory=RealDictCursor)
    conn.autocommit = False
    return conn


def get_setting(key, default=None):
    """Get a value from admin_settings table"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT value FROM admin_settings WHERE key = %s", (key,))
        row = cur.fetchone()
        conn.close()
        return row['value'] if row else default
    except Exception:
        return default


def init_database():
    """Initialize PostgreSQL schema if needed"""
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id TEXT UNIQUE NOT NULL,
            system_uid TEXT UNIQUE NOT NULL,
            referrer_id INTEGER REFERENCES users(id),
            caps_balance INTEGER DEFAULT 0 NOT NULL,
            is_blocked BOOLEAN DEFAULT FALSE,
            block_reason TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            last_activity TIMESTAMPTZ DEFAULT NOW(),
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            total_referrals INTEGER DEFAULT 0,
            total_earned_caps INTEGER DEFAULT 0,
            total_spent_caps INTEGER DEFAULT 0,
            ai_requests_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            referrer_id INTEGER NOT NULL REFERENCES users(id),
            referred_id INTEGER NOT NULL REFERENCES users(id),
            level INTEGER NOT NULL,
            commission_percent REAL NOT NULL,
            commission_earned REAL DEFAULT 0.00,
            caps_earned INTEGER DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(referrer_id, referred_id)
        );

        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            form_data TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            admin_notes TEXT,
            telegram_message_id TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            processed_at TIMESTAMPTZ
        );

        CREATE TABLE IF NOT EXISTS sos_requests (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            city TEXT NOT NULL,
            contact TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            admin_notes TEXT,
            telegram_message_id TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            resolved_at TIMESTAMPTZ
        );

        CREATE TABLE IF NOT EXISTS support_tickets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            message TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            admin_response TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS user_ai_sessions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            session_id TEXT NOT NULL,
            message_count INTEGER DEFAULT 0,
            is_blocked BOOLEAN DEFAULT FALSE,
            block_expires_at TIMESTAMPTZ,
            total_tokens_used INTEGER DEFAULT 0,
            total_cost_usd REAL DEFAULT 0.0,
            last_activity TIMESTAMPTZ DEFAULT NOW(),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_conversations (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            session_id TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            caps_spent INTEGER DEFAULT 0,
            tokens_used INTEGER DEFAULT 0,
            cost_usd REAL DEFAULT 0.0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_knowledge_base (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT NOT NULL,
            source TEXT,
            priority INTEGER DEFAULT 5,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_learned_data (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            context TEXT NOT NULL,
            importance_score INTEGER DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_learned_facts (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT DEFAULT 'user_interaction',
            priority INTEGER DEFAULT 1,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS lead_cards (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            telegram_id TEXT,
            field_name TEXT NOT NULL,
            field_value TEXT,
            collected_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, field_name)
        );

        CREATE TABLE IF NOT EXISTS ai_usage_log (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            tokens_in INTEGER DEFAULT 0,
            tokens_out INTEGER DEFAULT 0,
            cost REAL DEFAULT 0.0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS achievements (
            id SERIAL PRIMARY KEY,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT DEFAULT '🏆',
            reward_caps INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS user_achievements (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            achievement_id INTEGER NOT NULL REFERENCES achievements(id),
            earned_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(user_id, achievement_id)
        );

        CREATE TABLE IF NOT EXISTS offers (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            rate_from REAL NOT NULL,
            rate_to REAL NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS university_lessons (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            exam_questions TEXT,
            reward_caps INTEGER DEFAULT 30,
            order_index INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS university_progress (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            lesson_id INTEGER NOT NULL REFERENCES university_lessons(id),
            completed BOOLEAN DEFAULT FALSE,
            score INTEGER,
            attempts INTEGER DEFAULT 0,
            completed_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(user_id, lesson_id)
        );

        CREATE TABLE IF NOT EXISTS broadcasts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            photo_url TEXT,
            target_criteria TEXT,
            status TEXT DEFAULT 'draft',
            sent_count INTEGER DEFAULT 0,
            delivered_count INTEGER DEFAULT 0,
            failed_count INTEGER DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            sent_at TIMESTAMPTZ
        );

        CREATE TABLE IF NOT EXISTS admin_actions (
            id SERIAL PRIMARY KEY,
            admin_id TEXT NOT NULL,
            action_type TEXT NOT NULL,
            target_user_id INTEGER,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS pending_referrals (
            id SERIAL PRIMARY KEY,
            referred_user_id TEXT NOT NULL,
            referrer_id TEXT NOT NULL,
            processed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(referred_user_id, referrer_id)
        );

        CREATE TABLE IF NOT EXISTS admin_audit_log (
            id SERIAL PRIMARY KEY,
            admin_username TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            target_id TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS admin_messages (
            id SERIAL PRIMARY KEY,
            user_telegram_id TEXT NOT NULL,
            direction TEXT NOT NULL,
            message TEXT NOT NULL,
            admin_username TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS broadcast_history (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            photo_url TEXT,
            total_sent INTEGER DEFAULT 0,
            total_delivered INTEGER DEFAULT 0,
            total_failed INTEGER DEFAULT 0,
            admin_username TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_knowledge_base (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            file_type TEXT DEFAULT 'txt',
            priority INTEGER DEFAULT 1,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_learned_facts (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT DEFAULT 'user_interaction',
            priority INTEGER DEFAULT 1,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ai_usage_log (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            tokens_in INTEGER DEFAULT 0,
            tokens_out INTEGER DEFAULT 0,
            cost REAL DEFAULT 0.0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS shop_items (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            price_caps INTEGER NOT NULL,
            content_text TEXT,
            file_url TEXT,
            file_type TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)
        cur.execute("ALTER TABLE shop_items ADD COLUMN IF NOT EXISTS file_url TEXT")
        cur.execute("ALTER TABLE shop_items ADD COLUMN IF NOT EXISTS file_type TEXT")
        conn.commit()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS shop_purchases (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            price_paid INTEGER NOT NULL,
            purchased_at TIMESTAMP DEFAULT NOW()
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_cart (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, item_id)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS news_subscriptions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            telegram_id TEXT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            subscribed_at TIMESTAMPTZ DEFAULT NOW(),
            expires_at TIMESTAMPTZ,
            UNIQUE(user_id)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS balance_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            operation TEXT NOT NULL,
            description TEXT,
            balance_after INTEGER,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)

        try:
            cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS user_level TEXT DEFAULT 'basic'")
        except Exception:
            pass

        # Insert initial data if empty
        cur.execute("SELECT COUNT(*) as cnt FROM achievements")
        if cur.fetchone()['cnt'] == 0:
            cur.execute("""
            INSERT INTO achievements (code, name, description, icon, reward_caps) VALUES
            ('first_beer', '🍺 Первая кружка', 'Зарегистрироваться в системе', '🍺', 50),
            ('bartender', '🤝 Первый друг', 'Пригласить первого реферала (+30 крышек)', '🍻', 30),
            ('master_brewer', '👨‍🏫 Мастер рефералов', 'Пригласить 5 рефералов (+150 крышек)', '👨‍🍳', 150),
            ('university_grad', '🎓 Выпускник университета', 'Пройти все уроки', '🎓', 150),
            ('quiz_master', '🧠 Знаток пива', 'Сдать все экзамены на отлично', '🧠', 100),
            ('social_butterfly', '🦋 Душа компании', 'Пригласить 10 рефералов', '🦋', 300),
            ('chat_master', '💬 Болтун', 'Отправить 50 сообщений Михалычу', '💬', 75),
            ('early_bird', '🌅 Ранняя пташка', 'Войти в приложение в 6 утра', '🌅', 25),
            ('sos_helper', '🆘 Спасатель', 'Использовал SOS систему', '🆘', 30),
            ('application_sender', '📋 Заявитель', 'Отправил заявку на подключение', '📋', 25)
            """)

        cur.execute("SELECT COUNT(*) as cnt FROM offers")
        if cur.fetchone()['cnt'] == 0:
            cur.execute("""
            INSERT INTO offers (category, description, rate_from, rate_to) VALUES
            ('checks_1_10k', 'Чеки 1-10к', 12.00, 14.00),
            ('checks_10k_plus', 'Чеки 10к+', 8.00, 9.00),
            ('sim', 'Сим', 15.00, 15.00),
            ('qr_nspk', 'QR/НСПК', 12.00, 13.00)
            """)

        cur.execute("SELECT COUNT(*) as cnt FROM university_lessons")
        if cur.fetchone()['cnt'] == 0:
            _seed_university_lessons(cur)

        # Insert shop items if empty
        cur.execute("SELECT COUNT(*) as cnt FROM shop_items")
        if cur.fetchone()['cnt'] == 0:
            cur.execute("""
            INSERT INTO shop_items (category, title, description, price_caps, content_text) VALUES
            ('manuals', '📖 Базовый мануал по процессингу', 'Пошаговое руководство для новичков', 50, 'Скоро будет доступно'),
            ('private', '🔐 Приватная схема #1', 'Эксклюзивная схема заработка', 150, 'Скоро будет доступно'),
            ('schemes', '💡 Доп. схема: Арбитраж', 'Схема арбитражного заработка', 100, 'Скоро будет доступно'),
            ('training', '🎓 Продвинутый курс', 'Углубленное обучение процессингу', 200, 'Скоро будет доступно'),
            ('contacts', '📞 Контакты площадок', 'Список проверенных площадок', 75, 'Скоро будет доступно'),
            ('tables', '📊 Полезная табличка: Ставки', 'Сравнительная таблица ставок', 30, 'Скоро будет доступно')
            """)

        # Insert system admin user
        cur.execute("SELECT COUNT(*) as cnt FROM users WHERE telegram_id = 'SYSTEM'")
        if cur.fetchone()['cnt'] == 0:
            cur.execute("""
            INSERT INTO users (telegram_id, system_uid, first_name, last_name, username, caps_balance)
            VALUES ('SYSTEM', 'ADMIN', 'System', 'Admin', 'system_admin', 999999)
            """)

        # Insert default admin settings
        cur.execute("""
        INSERT INTO admin_settings (key, value) VALUES ('news_daily_cost', '10') ON CONFLICT (key) DO NOTHING;
        INSERT INTO admin_settings (key, value) VALUES ('ai_message_cost', '5') ON CONFLICT (key) DO NOTHING;
        """)

        # Enable RLS on all tables to block anon access via Supabase REST API
        rls_tables = ['users', 'referrals', 'pending_referrals', 'achievements', 'user_achievements',
                      'offers', 'ai_conversations', 'user_ai_sessions', 'ai_knowledge_base',
                      'ai_learned_facts', 'ai_usage_log', 'admin_audit_log', 'broadcast_history',
                      'admin_messages', 'admin_settings', 'lessons', 'user_lessons',
                      'applications', 'sos_requests', 'support_tickets', 'university_lessons',
                      'shop_items', 'shop_purchases', 'user_cart', 'news_subscriptions']
        for table in rls_tables:
            try:
                cur.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
                conn.commit()
            except Exception:
                conn.rollback()
        for table in rls_tables:
            try:
                cur.execute(f"""DO $$ BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = '{table}' AND policyname = 'deny_anon_{table}') THEN
                        EXECUTE format('CREATE POLICY deny_anon_{table} ON {table} FOR ALL TO anon USING (false)');
                    END IF;
                END $$""")
                conn.commit()
            except Exception:
                conn.rollback()

        # Add new columns to ai_learned_facts if missing
        try:
            cur.execute("ALTER TABLE ai_learned_facts ADD COLUMN IF NOT EXISTS fact TEXT")
            cur.execute("ALTER TABLE ai_learned_facts ADD COLUMN IF NOT EXISTS confidence REAL DEFAULT 1.0")
            cur.execute("ALTER TABLE ai_learned_facts ADD COLUMN IF NOT EXISTS learned_at TIMESTAMPTZ DEFAULT NOW()")
            cur.execute("ALTER TABLE ai_learned_facts ALTER COLUMN question DROP NOT NULL")
            cur.execute("ALTER TABLE ai_learned_facts ALTER COLUMN answer DROP NOT NULL")
        except Exception:
            conn.rollback()

        conn.commit()
        conn.close()
        logger.info("✅ Database initialized with RLS")
    except Exception as e:
        logger.error(f"DB init failed: {e}")


def _seed_university_lessons(cur):
    """Seed initial university lessons (вызывается из init_database)"""
    cur.execute("""
    INSERT INTO university_lessons (title, content, exam_questions, reward_caps, order_index) VALUES
    ('База процессинга',
     '🍺 <b>Урок 1: База процессинга</b>

<b>Что такое процессинг?</b>
Процессинг — это обработка финансовых транзакций между отправителем и получателем.',
     '[{"q":"Что такое процессинг?","options":["Обработка финансовых транзакций","Программирование сайтов","Майнинг криптовалют","Торговля на бирже"],"correct":0}]',
     15, 1)
    ON CONFLICT DO NOTHING
    """)
