# chats/middleware.py
from datetime import datetime, time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = 'requests.log'
        
    def __call__(self, request):
        # Get user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Log the request
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    Denies access between 9 PM (21:00) and 6 AM (06:00) with 403 Forbidden.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get current time
        current_time = datetime.now().time()
        
        # Define restricted hours: 9 PM (21:00) to 6 AM (06:00)
        start_restriction = time(21, 0)   # 9:00 PM
        end_restriction = time(6, 0)      # 6:00 AM
        
        # Check if current time is within restricted hours
        if (current_time >= start_restriction) or (current_time <= end_restriction):
            # Check if the request is for chat-related endpoints
            if self._is_chat_request(request):
                return HttpResponseForbidden(
                    "Access to messaging service is restricted between 9 PM and 6 AM. "
                    "Please try again during allowed hours."
                )
        
        response = self.get_response(request)
        return response
    
    def _is_chat_request(self, request):
        """
        Check if the request is for chat-related endpoints.
        """
        chat_paths = ['/api/conversations', '/api/messages', '/api/token']
        
        # Check if request path starts with any chat-related path
        return any(request.path.startswith(path) for path in chat_paths)
