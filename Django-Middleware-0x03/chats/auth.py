from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Overrides default JWT authentication to add extra checks, e.g. user active status.
        """
        user_auth_tuple = super().authenticate(request)

        if user_auth_tuple is None:
            return None

        user, token = user_auth_tuple

        if not user.is_active:
            raise AuthenticationFailed('User account is disabled.')

        # Add other custom checks here if needed

        return (user, token)