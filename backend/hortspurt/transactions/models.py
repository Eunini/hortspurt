from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
import datetime
class AddMoneyTransaction(models.Model):
    """Add money transaction object"""

    PAYMENT_METHODS = [
        ('USSD', 'USSD'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'pending'),
        ('successful', 'successful'),
        ('failed', 'failed')
    ]
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tr_id = models.CharField(max_length=200, blank=True, null=True)
    tr_ref = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=15, choices=PAYMENT_METHODS, default='USSD')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)