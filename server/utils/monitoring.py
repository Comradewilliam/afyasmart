from flask import request
import time
from functools import wraps
from .logger import api_logger

class APIMonitor:
    def __init__(self):
        self.requests = {}
        self.errors = {}
        self.response_times = {}
        
    def log_request(self, endpoint):
        """Log an API request"""
        if endpoint not in self.requests:
            self.requests[endpoint] = 0
        self.requests[endpoint] += 1
        
    def log_error(self, endpoint, error):
        """Log an API error"""
        if endpoint not in self.errors:
            self.errors[endpoint] = []
        self.errors[endpoint].append({
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'error': str(error)
        })
        
    def log_response_time(self, endpoint, duration):
        """Log API response time"""
        if endpoint not in self.response_times:
            self.response_times[endpoint] = []
        self.response_times[endpoint].append(duration)
        
    def get_stats(self):
        """Get monitoring statistics"""
        stats = {
            'requests': self.requests,
            'errors': {k: len(v) for k, v in self.errors.items()},
            'avg_response_times': {}
        }
        
        for endpoint, times in self.response_times.items():
            if times:
                avg_time = sum(times) / len(times)
                stats['avg_response_times'][endpoint] = f"{avg_time:.2f}ms"
                
        return stats

# Create monitor instance
monitor = APIMonitor()

def track_request(f):
    """Decorator to track API requests"""
    @wraps(f)
    def decorated(*args, **kwargs):
        endpoint = request.endpoint
        start_time = time.time()
        
        try:
            monitor.log_request(endpoint)
            response = f(*args, **kwargs)
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            monitor.log_response_time(endpoint, duration)
            
            # Log successful request
            api_logger.info(f"Request to {endpoint} completed in {duration:.2f}ms")
            
            return response
            
        except Exception as e:
            monitor.log_error(endpoint, e)
            # Log error
            api_logger.error(f"Error in {endpoint}: {str(e)}")
            raise
            
    return decorated
