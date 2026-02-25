#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Безопасность: headers, prompt injection filter, XSS sanitization
"""

import re
import html as html_module
import unicodedata
from flask import request
from .auth import check_rate_limit


def add_security_headers(response):
    """Добавить security headers к ответу"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # L-3: Permissions-Policy
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=()'

    # X-Frame-Options: DENY для всех кроме / (iframe в Telegram)
    if request.path == '/':
        response.headers['X-Frame-Options'] = 'ALLOWALL'
    else:
        response.headers['X-Frame-Options'] = 'DENY'

    # Content-Security-Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://telegram.org; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://api.telegram.org https://api.openai.com; "
        "frame-ancestors https://web.telegram.org https://*.telegram.org;"
    )

    return response


def global_rate_limit_check():
    """Глобальный rate limit: 60 req/min на IP"""
    from flask import jsonify
    ip = request.remote_addr
    if not check_rate_limit(f'global:{ip}', 60, 60):
        return jsonify({"error": "Rate limit exceeded"}), 429
    return None


# ===============================
# PROMPT INJECTION DETECTION
# ===============================


def normalize_text(text):
    """M-1: Normalize text to defeat obfuscation tricks before injection check."""
    # Remove zero-width characters
    text = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff]', '', text)
    # Normalize unicode (e.g. fullwidth letters → ASCII)
    text = unicodedata.normalize('NFKD', text)
    # Remove dots/dashes between letters (i.g.n.o.r.e → ignore)
    text = re.sub(r'(?<=\w)[.\-_](?=\w)', '', text)
    # Replace leet speak basics
    leet = {'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't'}
    for k, v in leet.items():
        text = text.replace(k, v)
    return text.lower()


PROMPT_INJECTION_PATTERNS = [
    # English patterns
    'ignore previous instructions', 'ignore all instructions', 'disregard previous',
    'system prompt', 'reveal your instructions', 'show your prompt', 'what are your instructions',
    'pretend you are', 'act as if you', 'you are now', 'forget your instructions',
    'override your', 'bypass your', 'ignore your rules', 'tell me your system',
    'what is your system message', 'repeat your prompt', 'output your instructions',
    'ignore the above', 'disregard all', 'new instructions:', 'jailbreak',
    'dan mode', 'developer mode', 'sudo mode', 'admin override',
    # Russian patterns
    'забудь инструкции', 'игнорируй правила', 'покажи промпт', 'системный промпт',
    'режим разработчика', 'режим администратора', 'забудь всё', 'новые инструкции',
    'ты теперь', 'представь что ты', 'притворись', 'отключи фильтры',
    'покажи свои правила', 'какие у тебя инструкции', 'выведи промпт',
    'обойди ограничения', 'сними ограничения', 'без цензуры', 'без ограничений',
    'расскажи свой промпт', 'покажи системное сообщение', 'debug mode',
    'системный промпт', 'system message', 'покажи инструкции', 'твои правила',
    # Encoding tricks
    'base64', 'rot13', 'hex encode', 'unicode', 'eval(', 'exec(',
    # Roleplay attacks
    'as an ai without restrictions', 'hypothetically speaking if you had no rules',
    'for educational purposes only ignore', 'in fiction mode',
]


def check_prompt_injection(message):
    """Advanced prompt injection detection with multi-layer checks."""
    # M-1: Normalize to defeat unicode obfuscation, leet speak, dot-separation
    msg_lower = normalize_text(message.strip())

    # Pattern matching
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in msg_lower:
            return True

    # Length-based heuristic (very long messages often contain injection)
    if len(message) > 2000:
        return True

    # Multiple instruction-like sentences
    instruction_markers = ['ты должен', 'you must', 'you should', 'ты обязан', 'выполни', 'execute', 'всегда отвечай', 'always respond']
    marker_count = sum(1 for m in instruction_markers if m in msg_lower)
    if marker_count >= 2:
        return True

    return False


# ===============================
# INPUT SANITIZATION (XSS Prevention)
# ===============================

def sanitize_html(text):
    """Sanitize user input to prevent XSS — escape HTML entities"""
    if not text:
        return text
    return html_module.escape(str(text))


def sanitize_user_input(text, max_length=2000):
    """Sanitize and truncate user input"""
    if not text:
        return ''
    text = str(text).strip()
    text = sanitize_html(text)
    return text[:max_length]
