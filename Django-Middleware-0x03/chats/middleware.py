import logging
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

# Configuring a logger for request logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")  # Logs saved in project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
    

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log every request with user details.
    Works with JWT authentication and session-based auth (like Django admin).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        user = None

        # Try to decode JWT token ---
        try:
            jwt_result = self.jwt_authenticator.authenticate(request)
            if jwt_result is not None:
                user, _ = jwt_result  # Extract user from JWT
        except Exception:
            # Ignore JWT errors to avoid breaking requests
            pass

        # Fallback to Django's session-based user (e.g., admin panel) ---
        if not user and hasattr(request, "user") and request.user.is_authenticated:
            user = request.user

        # Build user info string ---
        if user:
            if hasattr(user, "get_full_name") and user.get_full_name():
                name = user.get_full_name()
            elif hasattr(user, "username"):
                name = user.username
            else:
                name = str(user)

            user_info = f"{name} ({getattr(user, 'email', 'No Email')})"
        else:
            user_info = "Anonymous"

        # Log the request ---
        logger.info(f"{datetime.now()} - User: {user_info} - Path: {request.path}")

        # Continue processing request
        return self.get_response(request)
    

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app
    outside of 6 PM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response  # Called once when the server starts

    def __call__(self, request):
        # Get current server hour
        current_hour = datetime.now().hour

          # ALLOW only between 18:00 and 21:00
        if current_hour < 18 or current_hour >= 21:
            return HttpResponse(
                "<h1>403 Forbidden</h1>"
                "<p>Access to the messaging app is only allowed between "
                "<strong>6 PM and 9 PM</strong>.</p>",
                content_type="text/html",
                status=403
            )

        # Pass the request to the next middleware/view
        return self.get_response(request)