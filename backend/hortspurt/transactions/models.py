from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AddMoneyTransaction(models.Model):
    """Add money transaction object"""

    PAYMENT_METHODS = [
        ('U', 'USSD'),
    ]
    PAYMENT_STATUS = [
        ('P', 'PENDING'),
    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    tr_id = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=1, choices=PAYMENT_METHODS, default='U')
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default='P')
