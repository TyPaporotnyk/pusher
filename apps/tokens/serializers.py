from datetime import datetime
from typing import Any

from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class TokenSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["exp_time"] = (datetime.now() + refresh.lifetime).timestamp()

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
