from rest_framework import serializers

from user.models import AccountUser
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializers


class UserCreateSerializers(BaseUserCreateSerializers):
    class Meta(BaseUserCreateSerializers.Meta):
        fields = ['first_name', 'last_name','username', 'password', 'phone', 'email']
