from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from user.serializers import UserCreateSerializers

from user.models import AccountUser


# Create your views here.

class UserRegister(CreateAPIView):
    queryset = AccountUser.objects.all()
    serializer_class = UserCreateSerializers
