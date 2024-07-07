from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import AccountUser
from .models import Account


@receiver(post_save, sender=AccountUser)
def create_account(created, instance, **kwargs):
    if created:
        Account.objects.create(
            user=instance,
            account_number=instance.phone[1:]
        )
