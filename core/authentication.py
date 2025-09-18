from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or password is None:
            return None

        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            User().set_password(password)
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None



class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Priorité au header Authorization s'il est présent
        header_result = super().authenticate(request)
        if header_result is not None:
            return header_result

        # Sinon, on regarde dans les cookies
        raw_token = request.COOKIES.get('access_token')
        
        logger.debug(f"[CookieAuth] Token détecté dans cookies: {raw_token is not None}")
        
        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)

            if user is None:
                raise InvalidToken("Utilisateur introuvable")

            return (user, validated_token)

        except Exception as e:
            logger.warning(f"[CookieJWTAuthentication] Échec d'authentification via cookie: {e}")
            return None


# class CookieJWTMiddleware(MiddlewareMixin):
#     def process_request(self, request):
       
#         if not request.META.get('HTTP_AUTHORIZATION'):
#             access_token = request.COOKIES.get('access_token')
#             if access_token:
#                 request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        
#         return None

class CookieJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            access_token = request.COOKIES.get('access_token')
            if access_token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                logger.debug("[CookieJWTMiddleware] Authorization header injecté depuis cookie.")
                print("[CookieJWTMiddleware] Authorization header injecté depuis cookie.")
            else:
                logger.debug("[CookieJWTMiddleware] Aucun access_token dans les cookies.")
                print("[CookieJWTMiddleware] Aucun access_token dans les cookies.")
        else:
            logger.debug("[CookieJWTMiddleware] Header Authorization déjà présent.")
            print("[CookieJWTMiddleware] Header Authorization déjà présent.")
        
        return None