from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.

class AccountUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True, validators=[MaxLengthValidator(11), MinLengthValidator(11)])


class Address(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
