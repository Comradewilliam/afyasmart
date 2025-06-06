"""Routes package initialization"""
from .hospital_routes import register_hospital_routes
from .ai_routes import register_ai_routes
from .sms_routes import register_sms_routes
from .ussd_routes import register_ussd_routes
from .voice_routes import register_voice_routes

def register_routes(app):
    """Register all application routes"""
    register_hospital_routes(app)
    register_ai_routes(app)
    register_sms_routes(app)
    register_ussd_routes(app)
    register_voice_routes(app)
