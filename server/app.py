from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv
import os
from routes import register_routes
from database import init_db, Hospital, get_db, SessionLocal
from services.africa_talking import init_at_gateway
from utils.monitoring import monitor, track_request
# from api_docs import api  # TODO: Fix API docs later

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure app
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-key-12345')
app.config['JWT_ALGORITHM'] = os.getenv('JWT_ALGORITHM')

# Initialize admin interface
admin = Admin(app, name='AfyaSmart Admin', template_mode='bootstrap3')

# Get database session
db = SessionLocal()
admin.add_view(ModelView(Hospital, db))

# Initialize services
init_db()
init_at_gateway()

# Register API documentation
# TODO: Fix API docs later
# api.init_app(app)

# Register routes
register_routes(app)

# Add monitoring endpoint
@app.route('/api/monitor/stats')
@track_request
def get_monitor_stats():
    return jsonify(monitor.get_stats())

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AfyaSmart API is running"
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
