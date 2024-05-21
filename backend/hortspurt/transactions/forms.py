from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AddMoneyTransaction

class AddMoneyTrForm(forms.ModelForm):

    class Meta:
        model = AddMoneyTransaction
        fields = ('user', 'tr_id', 'amount', 'method', 'status')
    