# chats/middleware.py
from datetime import datetime
import logging
import os

# Setup logging
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create file handler if it doesn't exist
if not logger.handlers:
    file_handler = logging.FileHandler('requests.log')
    formatter = logging.Formatter('%(asctime)s - User: %(user)s - Path: %(path)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Log the request using logging module
        logger.info('', extra={'user': user, 'path': request.path})
        
        # Get the response
        response = self.get_response(request)
        
        return response
