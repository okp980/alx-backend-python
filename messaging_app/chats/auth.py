from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a user.
        """
        return super().authenticate(request)