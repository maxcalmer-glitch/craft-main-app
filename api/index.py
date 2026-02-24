#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 ENTERPRISE MAIN APPLICATION - Vercel + Supabase Edition
Modular architecture with security hardening.

Entry point: creates Flask app, registers blueprints, initializes DB.
"""

import os
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from flask_cors import CORS

from .config import config

# ===============================
# Sentry Error Monitoring
# ===============================
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        environment=os.environ.get('VERCEL_ENV', 'production'),
        release=config.VERSION if hasattr(config, 'VERSION') else '2.1',
        send_default_pii=False,
    )
from .database import init_database
from .security import add_security_headers, global_rate_limit_check
from .frontend import frontend_bp
from .routes_user import user_bp
from .routes_ai import ai_bp
from .routes_university import university_bp
from .routes_shop import shop_bp
from .routes_forms import forms_bp
from .routes_bot import bot_bp
from .routes_admin import admin_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===============================
# Flask App
# ===============================

app = Flask(__name__)
CORS(app, origins=[
    'https://web.telegram.org',
    'https://craft-main-app.vercel.app',
    'https://craft-test-app.vercel.app',
    'https://craft-admin-app.vercel.app',
    'https://craft-admin-test.vercel.app'
])

# ===============================
# Security Middleware
# ===============================

@app.after_request
def security_headers(response):
    return add_security_headers(response)

@app.before_request
def rate_limit():
    return global_rate_limit_check()

# ===============================
# Register Blueprints
# ===============================

app.register_blueprint(frontend_bp)
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(university_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(forms_bp)
app.register_blueprint(bot_bp)
app.register_blueprint(admin_bp)

# ===============================
# Initialize Database on Cold Start
# ===============================

try:
    if config.DATABASE_URL:
        init_database()
except Exception:
    pass

# ===============================
# Vercel Handler / Local Dev
# ===============================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=False)
# deploy trigger
