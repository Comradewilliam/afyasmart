import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create handlers
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Error log
    error_handler = RotatingFileHandler(
        os.path.join(logs_dir, f'error_{today}.log'),
        maxBytes=10000000,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    
    # Info log
    info_handler = RotatingFileHandler(
        os.path.join(logs_dir, f'info_{today}.log'),
        maxBytes=10000000,  # 10MB
        backupCount=5
    )
    info_handler.setLevel(logging.INFO)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)
    
    return logger

# Create loggers
api_logger = setup_logger('api')
db_logger = setup_logger('database')
ai_logger = setup_logger('ai')
sms_logger = setup_logger('sms')
ussd_logger = setup_logger('ussd')
voice_logger = setup_logger('voice')
