from rest_framework.authentication import TokenAuthentication
from core.models import AuthToken


class CustomTokenAuthentication(TokenAuthentication):
    model = AuthToken
