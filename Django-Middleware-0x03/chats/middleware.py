import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('request.log')
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