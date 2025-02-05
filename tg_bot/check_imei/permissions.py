from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class CheckToken(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.query_params.get('token', None)

        if token is None:
            raise ValidationError({"details":"Не указан token"}, code=401)

        token_obj = Token.objects.filter(key=token)

        if bool(token_obj):
            return True
        else:
            raise ValidationError({"details": "Token не обнаружен"}, code=401)
