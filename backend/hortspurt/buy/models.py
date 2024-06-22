from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class BuyAirtimeData(models.Model):
    """Buy transaction object"""

    NETWORK_PROVIDER = [
        ('MTN', 'MTN'),
        ('GLO', 'GLO'),
        ('Airtel', 'Airtel'),
        ('9mobile', '9mobile'),
    ]
    BUY_ACTION = [
        ('Received', 'Received'),
        ('Self', 'Self'),
        ('Gift', 'Gift')
    ]
    SERVICE = [
        ('Data', 'Data'),
        ('Airtime', 'Airtime'),
    ]
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(User, on_delete=models.PROTECT)
    tr_id = models.CharField(max_length=200, blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sponsor', null=True, blank=True)
    phone_no = models.CharField(max_length=11)
    price = models.PositiveIntegerField()
    amount = models.CharField(max_length=5)
    np = models.CharField(max_length=7, choices=NETWORK_PROVIDER)
    action = models.CharField(max_length=8, choices=BUY_ACTION)
    service = models.CharField(max_length=8, choices=SERVICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)