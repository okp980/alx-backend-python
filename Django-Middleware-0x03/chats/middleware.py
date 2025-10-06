import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponse, JsonResponse
from collections import defaultdict


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user if request.user.is_authenticated else "Anonymous"
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        response = self.get_response(request)
         # Code to be executed for each request/response after
        # the view is called.
        
        return response
    
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        current_time = datetime.now().time()
        if current_time < time(9, 0) or current_time > time(18, 0):
            return HttpResponse("Access denied", status=403)
        else:
            return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP addresses and their message timestamps
        self.ip_message_timestamps = defaultdict(list)
        # Rate limit: 5 messages per minute
        self.max_messages = 5
        self.time_window_minutes = 1
        
    def __call__(self, request):
        # Get the client IP address
        ip_address = self.get_client_ip(request)
        
        # Check if this is a POST request to a message endpoint
        if (request.method == 'POST' and 
            ('messages' in request.path or 'conversation-messages' in request.path)):
            
            current_time = datetime.now()
            
            # Clean old timestamps outside the time window
            cutoff_time = current_time - timedelta(minutes=self.time_window_minutes)
            self.ip_message_timestamps[ip_address] = [
                timestamp for timestamp in self.ip_message_timestamps[ip_address]
                if timestamp > cutoff_time
            ]
            
            # Check if IP has exceeded the rate limit
            if len(self.ip_message_timestamps[ip_address]) >= self.max_messages:
                return JsonResponse({
                    'error': 'Rate limit exceeded. You can only send 5 messages per minute.',
                    'retry_after': 60  # seconds
                }, status=429)
            
            # Add current timestamp to the IP's message history
            self.ip_message_timestamps[ip_address].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip