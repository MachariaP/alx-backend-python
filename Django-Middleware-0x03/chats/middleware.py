from datetime import datetime
import logging
import time
from django.http import HttpResponseForbidden, JsonResponse
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

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


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log each user's requests to a file.
    Logs timestamp, user, and request path.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        
    def __call__(self, request):
        # Log the request before processing
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Process the request and get response
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """
    Middleware that restricts access to the messaging app during certain hours.
    Denies access outside 6AM and 9PM (i.e., between 9PM and 6AM).
    """
    
    def __init__(self, get_response=None):
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


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware to limit chat messages per IP address within a time window.
    Implements rate limiting of 5 messages per minute per IP.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        # Rate limiting configuration
        self.limit = 5  # 5 messages
        self.window = 60  # 1 minute in seconds
        
    def __call__(self, request):
        # Only apply rate limiting to POST requests (chat messages)
        if request.method == 'POST':
            # Get client IP address
            ip_address = self.get_client_ip(request)
            
            if ip_address:
                # Create a unique key for this IP
                cache_key = f"chat_rate_limit_{ip_address}"
                
                # Get current timestamp
                current_time = time.time()
                
                # Get existing requests from cache or initialize empty list
                requests = cache.get(cache_key, [])
                
                # Remove requests outside the time window
                requests = [req_time for req_time in requests 
                           if current_time - req_time < self.window]
                
                # Check if limit exceeded
                if len(requests) >= self.limit:
                    return JsonResponse({
                        'error': 'Rate limit exceeded. Please wait before sending more messages.',
                        'limit': self.limit,
                        'window_seconds': self.window,
                        'retry_after': self.window
                    }, status=429)
                
                # Add current request timestamp
                requests.append(current_time)
                
                # Store updated requests in cache (expire after window time)
                cache.set(cache_key, requests, self.window)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware(MiddlewareMixin):  # CHANGED: lowercase 'p'
    """
    Middleware to check user's role before allowing access to specific actions.
    Only allows admin or moderator users for protected actions.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        # Define protected actions (URL patterns that require admin/moderator)
        self.protected_actions = [
            '/admin/',
            '/moderator/',
            '/api/delete/',
            '/api/ban/',
            '/api/manage/'
        ]
        
    def __call__(self, request):
        # Check if the current path matches any protected action
        if self.is_protected_action(request.path):
            # Check if user is authenticated and has admin/moderator role
            if not self.has_permission(request):
                return HttpResponseForbidden(
                    "You don't have permission to access this resource. "
                    "Admin or moderator role required."
                )
        
        response = self.get_response(request)
        return response
    
    def is_protected_action(self, path):
        """Check if the current path requires admin/moderator permissions"""
        return any(path.startswith(action) for action in self.protected_actions)
    
    def has_permission(self, request):
        """
        Check if user has admin or moderator role.
        Assumes user model has a 'role' field or uses groups.
        """
        if not request.user.is_authenticated:
            return False
        
        # Check if user has admin role (assuming role is stored in user profile)
        if hasattr(request.user, 'role'):
            return request.user.role in ['admin', 'moderator']
        
        # Alternative: Check groups if using Django's built-in groups
        elif request.user.groups.filter(name__in=['admin', 'moderator']).exists():
            return True
        
        # Alternative: Check is_staff for admin users
        elif request.user.is_staff:
            return True
        
        return False
