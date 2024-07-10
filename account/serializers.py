from django.core.validators import MaxLengthValidator, MinLengthValidator
from rest_framework import serializers
from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'transaction_time', 'description']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Account
        fields = ['account_number', 'balance', 'account_type', 'transactions']


class WithDrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    pin = serializers.CharField(validators=[MaxLengthValidator(4), MinLengthValidator(4)])


class DepositSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)


class TransferSerializer(serializers.Serializer):
    receiver_account_number = serializers.CharField(max_length=10)
    sender_account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    pin = serializers.CharField(validators=[MaxLengthValidator(4), MinLengthValidator(4)])


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'pin', 'account_type']
