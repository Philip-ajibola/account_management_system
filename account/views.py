import datetime
from decimal import Decimal

from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account, Transaction
from .serializers import AccountCreateSerializer, WithDrawSerializer, DepositSerializer, \
    TransferSerializer, TransactionSerializer


# Create your views here.

class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer


# # class ListAccount(ListCreateAPIView):
# #     queryset = Account.objects.all()
# #     serializer_class = AccountCreateSerializer
#
#     # def get(self, request):
#     #     accounts = Account.objects.all()
#     #     serializer = AccountSerializer(accounts, many=True)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
#     #
#     # def post(self, request):
#     #     serializer = AccountCreateSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class AccountDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer
# @api_view(['GET', 'POST'])
# def list_account(request):
#     if request.method == 'GET':
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = AccountCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def account_details(request, pk):
#     account = get_object_or_404(Account, pk=pk)
#     if request.method == 'GET':
#         serializer = AccountSerializer(account)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         serializer = AccountCreateSerializer(account, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         account.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class CreateAccount(CreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer
def transactionDetail(params, account_number, amount):
    transaction_details = {
        'request_time': datetime.datetime.now(),
        'success': True,
        'account_number': account_number,
        'amount': amount,
        'transaction_type': params,
        'message': 'Transaction SuccessFul'
    }
    return transaction_details


class Deposit(APIView):
    @staticmethod
    def post(request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        amount = Decimal(serializer.data['amount'])
        if amount <= 0:
            return Response(data={'success': True, 'message': 'Transaction Failed', 'account_number': account_number},
                            status=status.HTTP_400_BAD_REQUEST)
        account = get_object_or_404(Account, pk=account_number)
        balance = account.balance
        balance += amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        Transaction.objects.create(
            account=account,
            amount=amount
        )

        return Response(data=transactionDetail('CREDIT', account_number, amount), status=status.HTTP_200_OK)


class Withdraw(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = WithDrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        amount = Decimal(serializer.data['amount'])
        pin = serializer.data['pin']
        account = get_object_or_404(Account, pk=account_number)
        if account.pin == pin:
            if account.balance > amount:
                account.balance -= Decimal(amount)
                account.save()
            else:
                return Response(
                    data={"message": "Transaction unSuccessful", 'success': False, 'account_number': account_number},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "Invalid Credentials", 'success': False, 'account_number': account_number},
                            status=status.HTTP_400_BAD_REQUEST)

        Transaction.objects.create(
            account=account,
            amount=amount,
            transaction_type='DEB'
        )

        return Response(data=transactionDetail('DEBIT', account_number, amount), status=status.HTTP_200_OK)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class Transfer(APIView):
    @staticmethod
    @transaction.atomic
    def post(request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender_account_number = serializer.data['sender_account_number']
        receiver_account_number = serializer.data['receiver_account_number']
        amount = Decimal(serializer.data['amount'])
        pin = serializer.data['pin']
        receiver_account = get_object_or_404(Account, pk=receiver_account_number)
        sender_account = get_object_or_404(Account, pk=sender_account_number)
        if sender_account.balance < amount:
            return Response(data={'message': "Transfer Failed Due To Insufficient Balance", "success": False},
                            status=status.HTTP_400_BAD_REQUEST)
        sender_account.balance -= amount
        receiver_account.balance += amount
        receiver_account.save()
        sender_account.save()

        Transaction.objects.create(
            account=sender_account,
            amount=amount,
            transaction_type='TRANSFER'
        )
        return Response(data=transactionDetail('TRANSFER', sender_account_number, amount), status=status.HTTP_200_OK)


class CheckBalance(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        account = get_object_or_404(Account, user=user.id)
        response = {
            "request_time": datetime.datetime.now(),
            "success": True,
            "account_number": account.account_number,
            "balance": account.balance
        }
        message = f"""
        Hi {user.username},
        
        
        Your Balance is #{account.balance}
        
        
        Thank You For Banking With US!!!
        """
        send_mail("Mavericks Bank", message, 'noreply@maverickbank.com', [user.email])

        return Response(data=response, status=status.HTTP_200_OK)
