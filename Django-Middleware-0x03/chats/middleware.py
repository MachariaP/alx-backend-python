from datetime import datetime
import logging

# Set up logging configuration
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware to log each user's requests to a file.
    Logs timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Log the request before processing
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Process the request and get response
        response = self.get_response(request)
        
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    Denies access outside 6AM and 9PM (i.e., between 9PM and 6AM).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get current hour in 24-hour format
        current_hour = datetime.now().hour
        
        # Check if current time is between 9PM (21) and 6AM (6)
        # If current_hour >= 21 or current_hour < 6, deny access
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden(
                "Access denied: Chat is only available between 6AM and 9PM. "
                f"Current time: {datetime.now().strftime('%H:%M')}"
            )
        
        response = self.get_response(request)
        return response
