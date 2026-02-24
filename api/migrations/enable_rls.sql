-- CRAFT V2.0 — Enable Row Level Security on ALL tables
-- Blocks anon key access via Supabase REST API

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
ALTER TABLE pending_referrals ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE offers ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_ai_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_learned_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_learned_facts ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_usage_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE broadcast_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE sos_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE support_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE university_lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE university_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE broadcasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE shop_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE shop_purchases ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_cart ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE balance_history ENABLE ROW LEVEL SECURITY;

-- Deny all access for anon role
DO $$ 
DECLARE
    t TEXT;
    tables TEXT[] := ARRAY[
        'users', 'referrals', 'pending_referrals', 'achievements', 'user_achievements',
        'offers', 'ai_conversations', 'user_ai_sessions', 'ai_knowledge_base',
        'ai_learned_data', 'ai_learned_facts', 'ai_usage_log', 'admin_audit_log',
        'broadcast_history', 'admin_messages', 'admin_settings', 'admin_actions',
        'applications', 'sos_requests', 'support_tickets', 'university_lessons',
        'university_progress', 'broadcasts', 'shop_items', 'shop_purchases',
        'user_cart', 'lead_cards', 'balance_history'
    ];
BEGIN
    FOREACH t IN ARRAY tables LOOP
        IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = t AND policyname = 'deny_anon_' || t) THEN
            EXECUTE format('CREATE POLICY deny_anon_%I ON %I FOR ALL TO anon USING (false)', t, t);
        END IF;
    END LOOP;
END $$;
